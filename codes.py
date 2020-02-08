# LEFT FOR EASIER REFERENCE

x = """110 Restart marker reply.
120 Service ready in nnn minutes. # PASTE
125 Data connection already open; transfer starting.
150 File status okay; about to open data connection.
200 Command okay.
202 Command not implemented, superfluous at this site.
211 System status, or system help reply.
212 Directory status.
213 File status.
214 Help message.
215 NAME system type. # PASTE
220 Service ready for new user.
221 Service closing control connection. # Logged out if appropriate.
225 Data connection open; no transfer in progress.
226 Closing data connection. Requested file action successful (for example, file transfer or file
abort).
227 Entering Passive Mode (h1,h2,h3,h4,p1,p2).
230 User logged in, proceed.
250 Requested file action okay, completed.
257 "PATHNAME" created. # PASTE
331 User name okay, need password.
332 Need account for login.
350 Requested file action pending further information.
421 Service not available, closing control connection.
425 Can't open data connection.
426 Connection closed; transfer aborted.
450 Requested file action not taken.
451 Requested action aborted: local error in processing.
452 Requested action not taken. Insufficient storage space in system.
500 Syntax error, command unrecognized.
501 Syntax error in parameters or arguments.
502 Command not implemented.
503 Bad sequence of commands.
504 Command not implemented for that parameter.
530 Not logged in.
532 Need account for storing files.
550 Requested action not taken. # File unavailable (e.g., file not found, no access).
551 Requested action aborted: page type unknown.
552 Requested file action aborted.
553 Requested action not taken. File name not allowed."""
#
# if __name__ == '__main__':
#     lines = x.split('\n')
#     for line in lines:
#         code = line.split()[0]
#         ttt = f'''
# #     def make{code}(**kwargs) -> bytes:
#         """
#         {line}
#         """
#         return f'{line}'.encode()
#         '''
#         print(ttt)
#
#
# def make110(**kwargs) -> bytes:
#     """
#     110 Restart marker reply.
#     """
#     return f'110 Restart marker reply.'.encode()
#
#
# def make120(**kwargs) -> bytes:
#     """
#     120 Service ready in NNN minutes.
#     """
#     return f'120 Service ready in {kwargs["minutes"]} minutes.'.encode()
#
#
# def make125(**kwargs) -> bytes:
#     """
#     125 Data connection already open; transfer starting.
#     """
#     return f'125 Data connection already open; transfer starting.'.encode()
#
#
# def make150(**kwargs) -> bytes:
#     """
#     150 File status okay; about to open data connection.
#     """
#     return f'150 File status okay; about to open data connection.'.encode()
#
#
# def make200(**kwargs) -> bytes:
#     """
#     200 Command okay.
#     """
#     return f'200 Command okay.'.encode()
#
#
# def make202(**kwargs) -> bytes:
#     """
#     202 Command not implemented, superfluous at this site.
#     """
#     return f'202 Command not implemented, superfluous at this site.'.encode()
#
#
# def make211(**kwargs) -> bytes:
#     """
#     211 System status, or system help reply.
#     """
#     return f'211 System status, or system help reply.'.encode()
#
#
# def make212(**kwargs) -> bytes:
#     """
#     212 Directory status.
#     """
#     return f'212 Directory status.'.encode()
#
#
# def make213(**kwargs) -> bytes:
#     """
#     213 File status.
#     """
#     return f'213 File status.'.encode()
#
#
# def make214(**kwargs) -> bytes:
#     """
#     214 Help message.
#     """
#     return f'214 Help message.'.encode()
#
#
# def make215(**kwargs) -> bytes:
#     """
#     215 NAME system type.
#
#     NB: registry is here. But I guess it's okay to just send UNIX for this HW
#     """
#     return f'215 UNIX system type.'.encode()
#
#
# def make220(**kwargs) -> bytes:
#     """
#     220 Service ready for new user.
#     """
#     return f'220 Service ready for new user.'.encode()
#
#
# def make221(**kwargs) -> bytes:
#     """
#     221 Service closing control connection. # Logged out if appropriate.
#     """
#     return f'221 Service closing control connection. # Logged out if appropriate.'.encode()
#
#
# def make225(**kwargs) -> bytes:
#     """
#     225 Data connection open; no transfer in progress.
#     """
#     return f'225 Data connection open; no transfer in progress.'.encode()
#
#
# def make226(**kwargs) -> bytes:
#     """
#     226 Closing data connection. Requested file action successful (for example, file transfer
#     or file abort).
#     """
#     return f'226 Closing data connection. Requested file action successful (for example, ' \
#            f'file transfer or file abort).'.encode()
#
#
# def make227(**kwargs) -> bytes:
#     """
#     227 Entering Passive Mode (h1,h2,h3,h4,p1,p2).
#     """
#     return f'227 Entering Passive Mode (h1,h2,h3,h4,p1,p2).'.encode()
#
#
# def make230(**kwargs) -> bytes:
#     """
#     230 User logged in, proceed.
#     """
#     return f'230 User logged in, proceed.'.encode()
#
#
# def make250(**kwargs) -> bytes:
#     """
#     250 Requested file action okay, completed.
#     """
#     return f'250 Requested file action okay, completed.'.encode()
#
#
# def make257(**kwargs) -> bytes:
#     """
#     257 "PATHNAME" created. # PASTE
#     """
#     return f'257 "PATHNAME" created. # PASTE'.encode()
#
#
# def make331(**kwargs) -> bytes:
#     """
#     331 User name okay, need password.
#     """
#     return f'331 User name okay, need password.'.encode()
#
#
# def make332(**kwargs) -> bytes:
#     """
#     332 Need account for login.
#     """
#     return f'332 Need account for login.'.encode()
#
#
# def make350(**kwargs) -> bytes:
#     """
#     350 Requested file action pending further information.
#     """
#     return f'350 Requested file action pending further information.'.encode()
#
#
# def make421(**kwargs) -> bytes:
#     """
#     421 Service not available, closing control connection.
#     """
#     return f'421 Service not available, closing control connection.'.encode()
#
#
# def make425(**kwargs) -> bytes:
#     """
#     425 Can't open data connection.
#     """
#     return f'425 Can\'t open data connection.'.encode()
#
#
# def make426(**kwargs) -> bytes:
#     """
#     426 Connection closed; transfer aborted.
#     """
#     return f'426 Connection closed; transfer aborted.'.encode()
#
#
# def make450(**kwargs) -> bytes:
#     """
#     450 Requested file action not taken.
#     """
#     return f'450 Requested file action not taken.'.encode()
#
#
# def make451(**kwargs) -> bytes:
#     """
#     451 Requested action aborted: local error in processing.
#     """
#     return f'451 Requested action aborted: local error in processing.'.encode()
#
#
# def make452(**kwargs) -> bytes:
#     """
#     452 Requested action not taken. Insufficient storage space in system.
#     """
#     return f'452 Requested action not taken. Insufficient storage space in system.'.encode()
#
#
# def make500(**kwargs) -> bytes:
#     """
#     500 Syntax error, command unrecognized.
#     """
#     return f'500 Syntax error, command unrecognized.'.encode()
#
#
# def make501(**kwargs) -> bytes:
#     """
#     501 Syntax error in parameters or arguments.
#     """
#     return f'501 Syntax error in parameters or arguments.'.encode()
#
#
# def make502(**kwargs) -> bytes:
#     """
#     502 Command not implemented.
#     """
#     return f'502 Command not implemented.'.encode()
#
#
# def make503(**kwargs) -> bytes:
#     """
#     503 Bad sequence of commands.
#     """
#     return f'503 Bad sequence of commands.'.encode()
#
#
# def make504(**kwargs) -> bytes:
#     """
#     504 Command not implemented for that parameter.
#     """
#     return f'504 Command not implemented for that parameter.'.encode()
#
#
# def make530(**kwargs) -> bytes:
#     """
#     530 Not logged in.
#     """
#     return f'530 Not logged in.'.encode()
#
#
# def make532(**kwargs) -> bytes:
#     """
#     532 Need account for storing files.
#     """
#     return f'532 Need account for storing files.'.encode()
#
#
# def make550(**kwargs) -> bytes:
#     """
#     550 Requested action not taken. # File unavailable (e.g., file not found, no access).
#     """
#     return f'550 Requested action not taken. # File unavailable (e.g., file not found, ' \
#            f'no access).'.encode()
#
#
# def make551(**kwargs) -> bytes:
#     """
#     551 Requested action aborted: page type unknown.
#     """
#     return f'551 Requested action aborted: page type unknown.'.encode()
#
#
# def make552(**kwargs) -> bytes:
#     """
#     552 Requested file action aborted.
#     """
#     return f'552 Requested file action aborted.'.encode()
#
#
# def make553(**kwargs) -> bytes:
#     """
#     553 Requested action not taken. File name not allowed.
#     """
#     return f'553 Requested action not taken. File name not allowed.'.encode()
