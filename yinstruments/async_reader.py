from abc import abstractmethod

import serial


class ReaderError(Exception):
    """This is raised if the AsyncReader encounters an exception"""


class AsyncReader:
    """This class can be used for collecting text output asynchronously, and grouping into lines."""

    def __init__(self) -> None:
        self.partial_line = ""
        self.lines = []
        self.text = ""

    def get_line(self):
        """Return a line from the serial data if there is one available."""

        # If there is already a line in the list from a previous read, then return it.
        if self.lines:
            return self.lines.pop(0)

        # Otherwise get some new data and split it into lines, and return the first line.
        try:
            new_text = self._get_data()
        except serial.serialutil.SerialException as e:
            raise ReaderError(e)
        except UnicodeEncodeError as e:
            raise ReaderError(e)

        if not new_text:
            return None

        # Clean up string
        new_text = new_text.replace("\r", "")
        new_text = new_text.replace("\0", "")

        lines = new_text.splitlines(keepends=True)

        lines[0] = self.partial_line + lines[0]

        # Save last line
        if lines[-1][-1] != "\n":
            self.partial_line = lines.pop()
        else:
            self.partial_line = ""

        self.lines = lines

        if self.lines:
            return self.lines.pop(0).strip()

    def get_accumulate(self):
        """This function will accumulate received text,
        until clear_accumulate is called."""

        new_text = self._get_data()
        if new_text:
            self.text += new_text
        return self.text

    def clear_accumulate(self):
        self.text = ""

    @abstractmethod
    def _get_data(self):
        pass


class AsyncReaderUART(AsyncReader):
    """Subclass with support for reading from a UART"""

    def __init__(self, serial):
        super().__init__()
        self.serial = serial

    # def get_line(serial):
    #     """
    #     Raises: serial.serialutil.SerialException, UnicodeDecodeError, InvalidOutput
    #     """

    #     # Some text was received
    #     _PARTIAL_STR += uart_str

    #     # print("partial_str:", partial_str)

    #     # Check if it's a full line now
    #     if _PARTIAL_STR[-1] == "\n" and len(_PARTIAL_STR) > 1:
    #         # Remove new line
    #         msg = _PARTIAL_STR.strip()
    #         read_line_clear()

    #         # Process this line
    #         m = re.match("(" + "|".join(Severity.list()) + "): (.*)", msg)
    #         if not m:
    #             raise SerialInvalidOutput(msg)

    #         if m.group(1) in Severity.list():
    #             severity = Severity(m.group(1))
    #             return (severity, m.group(2).strip())
    #         else:
    #             # Should not be reachable
    #             assert False

    #     raise SerialNoFullLine

    def get_data(self):
        return self.serial.read_until()


class AsyncReaderSocket(AsyncReader):
    """Subclass with support for reading from a socket."""

    def __init__(self, socket):
        """Provide the already opened socket.  The socket will be put in non-blocking mode."""
        super().__init__()
        self.socket = socket
        self.socket.setblocking(0)

    def _get_data(self):
        try:
            return self.socket.recv(1024).decode("utf-8")
        except BlockingIOError:
            return None
