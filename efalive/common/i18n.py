'''
Created on 19.06.2019

Copyright (C) 2019-2019 Kay Hannay

This file is part of efaLiveSetup.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveSetup.  If not, see <http://www.gnu.org/licenses/>.
'''
import gettext

TRANSLATION = gettext.translation('efaLiveSetup', fallback=True)


def _(msg: str) -> str:
    return TRANSLATION.gettext(msg)


def _n(singular: str, plural: str, count: int) -> str:
    return TRANSLATION.ngettext(singular, plural, count)
