# FramewIRC

An IRC framework built upon Python 3's asyncio module.

Still immature, but a good foundation (I think).

Focuses on allowing the developer to pick only as much of the stack as required.


## Installation

```bash
pip install framewirc
```

## Rationale




## Quickstart

Here's a simple bot. Let's call it "snarkbot". Whenever it hears a particular
phrase, it responds with a gif.

It probably gets old rather quickly. (I think I may be writing autobiographical
documentation.)

```python
import asyncio

from framewirc import filters
from framewirc.client import Client
from framewirc.commands import PRIVMSG
from framewirc.handlers import basic_handlers


quips = {
    'shame': 'https://raw.githubusercontent.com/meshy/gifs/master/shame-bell.gif',
    'YOLO': 'https://raw.githubusercontent.com/meshy/gifs/master/who-said-yolo.gif',
}


@filters.command_whitelist(PRIVMSG)
def snarky_response(client, message):
    # See section "Still to come" for ideas on how this could be simplified.
    sender = message.prefix.split('!')[0]
    text = message.suffix

    for trigger, reposte in quips.items():
        if trigger in text:
            client.privmsg(sender, reposte)


class SnarkyClient(Client):
    handlers = basic_handlers + (snarky_response,)
    nick = 'snarkbot'
    real_name = 'framewirc bot'


SnarkyClient().connect_to('irc.example.com')
asyncio.get_event_loop().run_forever()
```


## Concepts



## Modules

### `client`

### `commands`

### `connection`

### `exceptions`

### `filters`

### `handlers`

### `message`

### `utils`


## Still to come

Features that I am hoping to implement in future:

- More layers of abstraction from the IRC protocol.

  In particular, I would like to call handlers with more intelligent kwargs
  when dealing with known types of events. This might mean that a handler of
  `PRIVMSG`s is sent `client, sender, recipient, text` rather than just
  `client, message`. That `sender` might also need some special treatment as
  the names of other users are often sent as `username!ident@host.example.com`
  but need to be replied to as simply `username`.

- Handle more text encodings.

  At the moment, the `to_unicode` method is a little prone to errors when
  `cChardet` provides a [non standard encoding][cchardet].

- Find a nicely overridable way to remove the `basic_handlers` boilerplate from
  `Client` subclasses that still allows ways to customise the behaviour.


[cchardet]: https://github.com/PyYoshi/cChardet/issues/13
