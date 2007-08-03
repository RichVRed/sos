### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sos.plugintools
import os

class ldap(sos.plugintools.PluginBase):
    """LDAP related information
    """
    def get_ldap_opts(self):
        # capture /etc/openldap/ldap.conf options in dict
        # FIXME: possibly not hardcode these options in?
        ldapopts=["URI","BASE","TLS_CACERTDIR"]
        results={}
        tmplist=[]
        for i in ldapopts:
            t=fileGrep(r"^%s*" % i,"/etc/openldap/ldap.conf")
            for x in t:
                tmplist.append(x.split(" "))
        for i in tmplist:
            results[i[0]]=i[1].rstrip("\n")
        return results

    def diagnose(self):
        # Validate ldap client options
        ldapopts=self.get_ldap_opts()
        try:
            os.stat(ldapopts["TLS_CACERTDIR"])
        except:
            self.addDiagnose("%s does not exist and can cause connection issues "+
                             "involving TLS" % ldapopts["TLS_CACERTDIR"])

    def setup(self):
        self.addCopySpec("/etc/ldap.conf")
        self.addCopySpec("/etc/openldap")
        return

    def postproc(self):
        self.doRegexSub("/etc/ldap.conf", r"(\s*bindpw\s*)\S+", r"\1***")
        return
