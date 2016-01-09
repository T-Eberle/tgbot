# A Python Telegram Bot
[![Build Status](https://travis-ci.org/T-Eberle/tgbot.svg?branch=master)](https://travis-ci.org/T-Eberle/tgbot)

Welcome to a UWSGI based abstract Telegram Bot. With this framework you are easily able to set up a complete Telegram Bot with self made commands without a lot of extra work. All abstract commands are implemented as GET-Responses as explained on https://core.telegram.org/bots/api. This means you don't need to have experience in HTTP Requests or PHP: All you need is python.

In the next few chapters I will explain you all the Features and how to properly set up the bot.


#Set Up
First of all, as we are talking about an *abstract* bot you first need to *implement* this package.

**For programming with the bot, you need the following:**

1. At least Python 3.X
2. A good supported Python IDE (for example PyCharm)
3. This python package , available on pypi

An example implementation of this bot will be soon available in the example folder.

**For using your bot implemenation on a real server**

1. At least Python 3.X
2. Install this package with pip install xxxx
3. Install uwsgi with pip install uwsgi

*Warning*: It's recommended that you install all packages used for your bot on a virtual environment to not mess up your OS. All infos about Virtual Environments can be read on http://docs.python-guide.org/en/latest/dev/virtualenvs/. With virtual environments you can keep all the used requirements only for this project / bot.

More instructions will follow.

#Features
## Commands and Inline Commands

This Bot support both the normal commands and the newly added inline commands. To add new commands you simply create methods inside either a Command- or InlineCommandClass. The name of the method is the command itself. To add more command- inlinecommandclasses to your bot you simply add the to the lists which you give the class TGBotWSGI when you initialise the bot. For more information check the example.
## Configuration
### UWSGI
### Bot
## Logging
## Redis

More Documentation will follow.


