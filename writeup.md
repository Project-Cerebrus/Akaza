# What is this?
A writeup on each section of the three modules

## Writeup:

### Economy:
The economy section was created using a mix of json and python. Simply put upon meeting the events described in the README, it gave x amount of doggocoins and dumped the values

The buy system was made through having an `item: []` list in the json file, so it would append the values into the json file when bought

Then the use system would test for the item and then follow the function

### Donations:
A simple mix of adding and subtracting amounts in json

### Giveaways:
The main issue was that the giveaway system was not too efficient and a on_message system would not work too well either. This created a problem until it was thought off that we should use a background task. Next this created the problem of how to gain ctx in a background task. To achieve this we put a on_message to loop the task once so it would be able to loop with ctx permissions. Since we have json values now we can edit it accordingly and make a command which showcases all giveaways as well as better editing, requirement roles and an amount of winners. This is a fairly complex system which is a bit unstable and this is only being used since this is the only solution without using a sql server which would take time and space. In other words, this is a lightweight giveaway cog which uses a complex background task system.