# Changelog for `framewirc`

This project is in alpha. I plan to adhere to [semantic versioning][semver]
once the API is stable.

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
