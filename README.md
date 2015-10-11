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

Unfortunately, there's no ["One True Way"][xkcd-standards] when it comes to
IRC. Many networks and servers have their own way of doing things that are not
entirely compatible with others. There's nothing wrong with this, exactly, but
it does mean that until this library is a little more mature, it might not
correctly deal with all these eccentricities. If you find an issue that is not
correctly dealt with, please [log an issue on github][github-issues].


### IRC message format

It's probably useful to have some idea of how the IRC protocol works. All
messages in both directions must adhere to the (simple) rules:

- Messages are represented as bytes.

  There is no default encoding, so sometimes one just has to guess! To guess
  how to turn these streams of bytes into Python strings, we have elected to
  use [`cChardet`][cchardet-home] for this in `utils.to_unicode`.

- Messages have a relatively simple structure.

  Generally, a message can be seen to have four distinct parts: a prefix, a
  command, a number of parameters, and a suffix. The parts that are required
  depend on the command. Only the command is always required. This is the
  structure of a message:

  ```
  :colon-indicated-prefix COMMAND some parameters :Suffix following the colon
  ```

  We represent the messages that come from the network with our own subclass of
  `bytes` called `ReceivedMessage`. It has `prefix`, `command`, `parameters`,
  and `suffix` added for convinience. Each of these attributes represents the
  relevant message parts as a unicode string (except `parameters`, which is a
  tuple of strings).

- Messages have a maximum length of 512 bytes.

  This means that when we want to send something longer to the network, we have
  to split it up into smaller chunks. This can be done using
  `utils.chunk_message`.


### Connecting

To connect to an IRC network, you will generally create a `Client` object, and
tell it to `connect_to` the network of your choice. This in turn creates a
`Connection`, and an `asyncio.Task` that will be invoked in the event loop.

Once the loop has started (or if it already has), the `Connection` will attempt
to connect to the network. Once it does, the `Client` will be responsible for
completing the process by telling the network the nick and real name of the
client.

If there are any actions that need to be completed on connection, this is
probably the time to do it. The `Client.on_connect` method can be overridden to
add things like connecting to particular rooms, or sending a password to an
authentication bot. (Don't forget to call `super` though!)


### Handling messages

When the `Connection` receives a message, the `Client` will send that message
(and itself) to every one of its `handers` in turn. This allows them to make a
decision about how they will deal with the message.

As most of your handlers will not need to deal with every message that comes
in, we can remove the boilerplate of `if message.command == MYCOMMAND` through
use of the decorators in the `filters` module. The `command_whitelist` filter
only allows messages through to the handler that are in its whitelist. The
`command_blacklist` does the opposite. eg:

```python
# Rather than this:
def my_command_handler(client, message):
    if message.command != MYCOMMAND:
        return
    do_useful_logic(message)

# It's nicer to have this:
@command_whitelist(MYCOMMAND):
def my_simpler_command_handler(client, message):
    do_useful_logic(message)
```


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
  `cChardet` provides a [non standard encoding][cchardet-issue-13].

- Find a nicely overridable way to remove the `basic_handlers` boilerplate from
  `Client` subclasses that still allows ways to customise the behaviour.


[cchardet-home]: https://github.com/PyYoshi/cChardet/
[cchardet-issue-13]: https://github.com/PyYoshi/cChardet/issues/13
[github-issues]: https://github.com/meshy/framewirc/issues/
[xkcd-standards]: https://xkcd.com/927/
