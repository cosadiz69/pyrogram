# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram.api import functions, types
from ...ext import BaseClient, utils


class Filters:
    ALL = "all"
    KICKED = "kicked"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"


class GetChatMembers(BaseClient):
    async def get_chat_members(self,
                               chat_id: int or str,
                               offset: int = 0,
                               limit: int = 200,
                               query: str = "",
                               filter: str = Filters.ALL):
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            return utils.parse_chat_members(
                await self.send(
                    functions.messages.GetFullChat(
                        peer.chat_id
                    )
                )
            )
        elif isinstance(peer, types.InputPeerChannel):
            filter = filter.lower()

            if filter == Filters.ALL:
                filter = types.ChannelParticipantsSearch(q=query)
            elif filter == Filters.KICKED:
                filter = types.ChannelParticipantsKicked(q=query)
            elif filter == Filters.RESTRICTED:
                filter = types.ChannelParticipantsBanned(q=query)
            elif filter == Filters.BOTS:
                filter = types.ChannelParticipantsBots()
            elif filter == Filters.RECENT:
                filter = types.ChannelParticipantsRecent()
            elif filter == Filters.ADMINISTRATORS:
                filter = types.ChannelParticipantsAdmins()
            else:
                raise ValueError("Invalid filter \"{}\"".format(filter))

            return utils.parse_chat_members(
                await self.send(
                    functions.channels.GetParticipants(
                        channel=peer,
                        filter=filter,
                        offset=offset,
                        limit=limit,
                        hash=0
                    )
                )
            )
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))
