# Changelog for `framewirc`

This project is in alpha. I plan to adhere to [semantic versioning][semver]
once the API is stable.

## Unreleased
- CHANGED: Renamed `framewirc.message` module to `framewirc.messages`.

- CHANGED: Moved `to_bytes` from `framewirc.utils` to `framewirc.strings`.

- CHANGED: Moved `to_unicode` from `framewirc.utils` to `framewirc.strings`.

- CHANGED: Moved `chunk_message` from `framewirc.utils` to `framewirc.messages`.

- REMOVED: Support for Python `3.4` has been removed.

- ADDED: Support for Python `3.5` and `3.6` has been added.

- ADDED: `client.Client.privmsg` now takes `third_person`.

  This can be used to send third person messages. (`/me likes this :D`)

- ADDED: `message.make_privmsgs` now takes `third_person`.

  This can be used to create third person messages. (`/me also likes this :D`)

- ADDED: `message.make_privmsgs` now takes `mask_length`.

  This accounts for the network added overhead (sender) on messages.

- ADDED: `client.Client` now has `mask_length` attribute.

  Allows fine-tuning of sender mask overhead size for splitting messages.

- ADDED: `client.Client.join`.

- ADDED: `client.Client.part`.

- FIXED: `parsers.nick`.

  No longer falls over on nicks that are already just nicks (no ident, etc).

- FIXED: `client.Client.connect_to`.

  No longer directly instantiates `asycio.Task`. This allows custom loops to
  customise `Task`. See #18.

- FIXED: `utils.to_bytes` and `utils.to_unicode` now throw the correct error.

  Previously, when passed an instance of the wrong type, these functions would
  throw `AttributeError`. Now, correctly, they throw `TypeError`.

- FIXED: `messages.chunk_bytes` no longer loses spaces when splitting lines.

- FIXED: `messages.chunk_bytes` no longer splits lines that fit exactly.

## v0.1.0

- CHANGED: Renamed `filters.command_blacklist` to `filters.deny`.

- CHANGED: Renamed `filters.command_whitelist` to `filters.allow`.

- CHANGED: `ReceivedMessage.suffix`

  This is no longer a unicode string, as it was too presumptious to guess the
  encoding. This is now left to the programmer to decide, allowing them to do
  things such as change default encoding per channel.

- ADDED: `parsers.apply_kwargs_parser`

  A handler decorator that takes a parser, and passes the resulting dictionary
  to the handler as kwargs. The parser should accept all kwargs.

- ADDED: `parsers.apply_message_parser`

  A handler decorator that takes a parser, and passes the resulting dictionary
  to the handler as kwargs. The parser should accept only a `message` kwarg.

- ADDED: `parsers.is_channel`.

  A function to determine of a string is a valid channel name.

- ADDED: `parsers.nick`.

  A function that takes a `nick!ident@host` string (or similar), and returns a
  dictionary of components.

- ADDED: `parsers.privmsg`.

  A function that splits a `PRIVMSG` command into a dictionary of semantically
  named attributes.

- ADDED: `utils.to_unicode` now takes encoding suggestions.

  An iterable of Preferred character encodings can now be passed in.

## v0.0.1

Initial release.


[semver]: http://semver.org/spec/v2.0.0.html
