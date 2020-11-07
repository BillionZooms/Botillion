from discord.ext import commands

import os
import json

def tempchannelAdd(userid, channelid):
    with open('tempchannel.json', 'r') as f:
        try:
            d = json.load(f)
            if userid in d['Owners'].keys():
                l = d['Owners'].get(userid)
                l.append(channelid)
                d['Owners'][userid] = l
            else:
                idlist = [channelid]
                di = {userid : idlist}
                d['Owners'].update(di)
        except:
            idlist = []
            idlist.append(channelid)
            d = {
                'Owners' : {
                    userid : idlist
                }
            }
        f.close()
    with open('tempchannel.json', 'w') as f:
        json.dump(d, f, indent=2)
        f.close()