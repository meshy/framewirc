import enum


@enum.unique
class Command(enum.Enum):
    ########
    # BASE #
    ########

    # Registration
    NICK = b'NICK'
    PASS = b'PASS'
    QUIT = b'QUIT'
    USER = b'USER'  # Sent when registering a new user.

    # Channel ops
    INVITE = b'INVITE'
    JOIN = b'JOIN'
    KICK = b'KICK'
    LIST = b'LIST'
    MODE = b'MODE'
    NAMES = b'NAMES'
    PART = b'PART'
    TOPIC = b'TOPIC'

    # Server ops
    ADMIN = b'ADMIN'
    CONNECT = b'CONNECT'
    INFO = b'INFO'
    LINKS = b'LINKS'
    OPER = b'OPER'
    REHASH = b'REHASH'
    RESTART = b'RESTART'
    SERVER = b'SERVER'  # Sent when registering as a server.
    SQUIT = b'SQUIT'
    STATS = b'STATS'
    SUMMON = b'SUMMON'
    TIME = b'TIME'
    TRACE = b'TRACE'
    VERSION = b'VERSION'
    WALLOPS = b'WALLOPS'

    # Sending messages
    NOTICE = b'NOTICE'
    PRIVMSG = b'PRIVMSG'

    # User queries
    WHO = b'WHO'
    WHOIS = b'WHOIS'
    WHOWAS = b'WHOWAS'

    # Misc
    ERROR = b'ERROR'
    KILL = b'KILL'
    PING = b'PING'
    PONG = b'PONG'

    # Optional
    AWAY = b'AWAY'
    USERS = b'USERS'
    USERHOST = b'USERHOST'
    ISON = b'ISON'  # "Is on"

    ###########
    # REPLIES #
    ###########

    # 001 to 004 are sent to a user upon successful registration.
    RPL_WELCOME = b'001'
    RPL_YOURHOST = b'002'
    RPL_CREATED = b'003'
    RPL_MYINFO = b'004'

    # Sent by the server to suggest an alternative server when full or refused.
    RPL_BOUNCE = b'005'

    # Reply to the USERHOST command.
    RPL_USERHOST = b'302'

    # Reply to the ISON command (to see if a user "is on").
    RPL_ISON = b'303'

    # Sent to any client sending a PRIVMSG to a client which is away.
    RPL_AWAY = b'301'

    # Acknowledgements of the AWAY command.
    RPL_UNAWAY = b'305'
    RPL_NOWAWAY = b'306'

    # Replies to a WHOIS message.
    RPL_WHOISUSER = b'311'
    RPL_WHOISSERVE = b'312'
    RPL_WHOISOPERATOR = b'313'
    RPL_WHOISIDLE = b'317'
    RPL_ENDOFWHOIS = b'318'
    RPL_WHOISCHANNELS = b'319'

    # Replies to WHOWAS command. See also ERR_WASNOSUCHNICK.
    RPL_WHOWASUSER = b'314'
    RPL_ENDOFWHOWAS = b'369'

    # Replies to LIST command. Note that 321 is obsolete and unused.
    RPL_LISTSTART = b'321'
    RPL_LIST = b'322'
    RPL_LISTEND = b'323'

    # Replies to MODE. I don't understand the spec of 325!
    RPL_CHANNELMODEIS = b'324'
    RPL_UNIQOPIS = b'325'
    RPL_INVITELIST = b'346'
    RPL_ENDOFINVITELIST = b'347'
    RPL_EXCEPTLIST = b'348'
    RPL_ENDOFEXCEPTLIST = b'349'
    RPL_BANLIST = b'367'
    RPL_ENDOFBANLIST = b'368'
    RPL_UMODEIS = b'221'

    # Replies to TOPIC.
    RPL_NOTOPIC = b'331'
    RPL_TOPIC = b'332'

    # Acknowledgement of INVITE command.
    RPL_INVITING = b'341'

    # Acknowledgement of SUMMON command.
    RPL_SUMMONING = b'342'

    # Reply to VERSION.
    RPL_VERSION = b'351'

    # Reply to WHO.
    RPL_WHOREPLY = b'352'
    RPL_ENDOFWHO = b'315'

    # Reply to NAMES.
    RPL_NAMREPLY = b'353'
    RPL_ENDOFNAMES = b'366'

    # Reply to LINKS.
    RPL_LINKS = b'364'
    RPL_ENDOFLINKS = b'365'

    # Reply to INFO.
    RPL_INFO = b'371'
    RPL_ENDOFINFO = b'374'

    # Reply to MOTD. Also usually sent upon successful registration.
    RPL_MOTDSTART = b'375'
    RPL_MOTD = b'372'
    RPL_ENDOFMOTD = b'376'

    # Acknowledgement of OPER.
    RPL_YOUREOPER = b'381'

    # Acknowledgement of REHASH.
    RPL_REHASHING = b'382'

    # Reply to SERVICE upon successful registration.
    RPL_YOURESERVICE = b'383'

    # Reply to TIME.
    RPL_TIME = b'391'

    # Replies to USERS.
    RPL_USERSSTART = b'392'
    RPL_USERS = b'393'
    RPL_ENDOFUSERS = b'394'
    RPL_NOUSERS = b'395'

    # Replies to TRACE.
    RPL_TRACELINK = b'200'
    RPL_TRACECONNECTING = b'201'
    RPL_TRACEHANDSHAKE = b'202'
    RPL_TRACEUNKNOWN = b'203'
    RPL_TRACEOPERATOR = b'204'
    RPL_TRACEUSER = b'205'
    RPL_TRACESERVER = b'206'
    RPL_TRACESERVICE = b'207'
    RPL_TRACENEWTYPE = b'208'
    RPL_TRACECLASS = b'209'
    RPL_TRACERECONNECT = b'210'
    RPL_TRACELOG = b'261'
    RPL_TRACEEND = b'262'

    # Reply to STATS. See also ERR_NOSUCHSERVER.
    RPL_STATSLINKINFO = b'211'
    RPL_STATSCOMMANDS = b'212'
    RPL_ENDOFSTATS = b'219'
    RPL_STATSUPTIME = b'242'
    RPL_STATSOLINE = b'243'

    # Reply to SERVLIST.
    RPL_SERVLIST = b'234'
    RPL_SERVLISTEND = b'235'

    # Reply to LUSERS.
    RPL_LUSERCLIENT = b'251'
    RPL_LUSEROP = b'252'
    RPL_LUSERUNKNOWN = b'253'
    RPL_LUSERCHANNELS = b'254'
    RPL_LUSERME = b'255'

    # Reply to ADMIN.
    RPL_ADMINME = b'256'
    RPL_ADMINLOC1 = b'257'
    RPL_ADMINLOC2 = b'258'
    RPL_ADMINEMAIL = b'259'

    # Sent when a server drops a command without processing it.
    RPL_TRYAGAIN = b'263'

    ##########
    # ERRORS #
    ##########

    ERR_NOSUCHNICK = b'401'
    ERR_NOSUCHSERVER = b'402'
    ERR_NOSUCHCHANNEL = b'403'
    ERR_CANNOTSENDTOCHAN = b'404'
    ERR_TOOMANYCHANNELS = b'405'
    ERR_WASNOSUCHNICK = b'406'
    ERR_TOOMANYTARGETS = b'407'
    ERR_NOSUCHSERVICE = b'408'
    ERR_NOORIGIN = b'409'
    ERR_NORECIPIENT = b'411'
    ERR_NOTEXTTOSEND = b'412'
    ERR_NOTOPLEVEL = b'413'
    ERR_WILDTOPLEVEL = b'414'
    ERR_BADMASK = b'415'
    ERR_UNKNOWNCOMMAND = b'421'
    ERR_NOMOTD = b'422'
    ERR_NOADMININFO = b'423'
    ERR_FILEERROR = b'424'
    ERR_NONICKNAMEGIVEN = b'431'
    ERR_ERRONEUSNICKNAME = b'432'
    ERR_NICKNAMEINUSE = b'433'
    ERR_NICKCOLLISION = b'436'
    ERR_UNAVAILRESOURCE = b'437'
    ERR_USERNOTINCHANNEL = b'441'
    ERR_NOTONCHANNEL = b'442'
    ERR_USERONCHANNEL = b'443'
    ERR_NOLOGIN = b'444'
    ERR_SUMMONDISABLED = b'445'
    ERR_USERSDISABLED = b'446'
    ERR_NOTREGISTERED = b'451'
    ERR_NEEDMOREPARAMS = b'461'
    ERR_ALREADYREGISTRED = b'462'
    ERR_NOPERMFORHOST = b'463'
    ERR_PASSWDMISMATCH = b'464'
    ERR_YOUREBANNEDCREEP = b'465'
    ERR_YOUWILLBEBANNED = b'466'
    ERR_KEYSET = b'467'
    ERR_CHANNELISFULL = b'471'
    ERR_UNKNOWNMODE = b'472'
    ERR_INVITEONLYCHAN = b'473'
    ERR_BANNEDFROMCHAN = b'474'
    ERR_BADCHANNELKEY = b'475'
    ERR_BADCHANMASK = b'476'
    ERR_NOCHANMODES = b'477'
    ERR_BANLISTFULL = b'478'
    ERR_NOPRIVILEGES = b'481'
    ERR_CHANOPRIVSNEEDED = b'482'
    ERR_CANTKILLSERVER = b'483'
    ERR_RESTRICTED = b'484'
    ERR_UNIQOPPRIVSNEEDED = b'485'
    ERR_NOOPERHOST = b'491'
    ERR_UMODEUNKNOWNFLAG = b'501'
    ERR_USERSDONTMATCH = b'502'