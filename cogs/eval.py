from discord.ext import commands
import io, textwrap, traceback
from library import constants
from contextlib import redirect_stdout

def cleanup_code(content):
	"""Automatically removes code blocks from the code."""
	# remove ```py\n```
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:-1])

	# remove `foo`
	return content.strip('` \n')


class eval(commands.Cog, name='evaluation'):
	def __init__(self, bot):
		self.bot = bot
		self._last_result = None
	
	@commands.command(pass_context=True, hidden=True, name='eval')
	async def _eval(self, ctx, *, body: str):
		if ctx.author.id not in constants.DEVS:
			return
		"""Evaluates a code"""

		env = {
			'bot': self.bot,
			'ctx': ctx,
			'channel': ctx.channel,
			'author': ctx.author,
			'guild': ctx.guild,
			'message': ctx.message,
			'_': self._last_result
		}

		env.update(globals())

		body = cleanup_code(body)
		stdout = io.StringIO()

		to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f'**Error:**\n```py\n{value}{traceback.format_exc()}\n```')
		else:
			value = stdout.getvalue()
			try:
				await ctx.message.add_reaction('\u2705')
			except:
				pass

			if ret is None:
				if value:
					await ctx.send(f'```py\n{value}\n```')
			else:
				self._last_result = ret
				await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    bot.add_cog(eval(bot))