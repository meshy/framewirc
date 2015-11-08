# Changelog for `framewirc`

This project is in alpha. I plan to adhere to [semantic versioning][semver]
once the API is stable.

## Unreleased

- ADDED: `parsers.is_channel`.

  A function to determine of a string is a valid channel name.

- ADDED: `parsers.nick`.

  A function that takes a `nick!ident@host` string (or similar), and returns a
  dictionary of components.

- ADDED: `parsers.privmsg`.

  A function that splits a `PRIVMSG` command into a dictionary of semantically
  named attributes.


## v0.0.1

Initial release.


[semver]: http://semver.org/spec/v2.0.0.html
