import time
import sys
import praw
from webhooks import *
from replies import *
from DM2_CommonUtils import hours_since
from DM2_CommonUtils import get_reddit_instance
from spazutils import Usernotes
import requests
import pprint
from modmaillists import *
reddit = get_reddit_instance("")
sub = reddit.subreddit('')
word = "karma"
removal_list = ["A /r/dankmemes submission has been removed!"]
dox_list = ["phone number", "dox", "my address", "brigading", "brigade"]
ban_list = ["banned", "ban", "unban"]
bancommand_list = ["!ban"]
thank_list = ["thank you", "thanks!", "thanks", "thank you!"]







while True:
    try:
        #Look through all modmail messages
        for x in sub.modmail.conversations(state="all", limit=1000):
            userlower = "this is here so if the below part throws an exception it doesnt ruin everything"
            try:
                test = (x.user)
                userlower = (str(test.name).lower())
            except Exception as e: 
                print(f"{e} {x.id}")
                #if message is automated notification, forward to discord and archive
                if "A /r/dankmemes submission has been removed!" in x.subject:
                    print('automod removal')
                    for message in x.messages:
                        sub.modmail(x.id).archive()
                        requests.post(webhook1, data={"content":"New automod removal: https://mod.reddit.com/mail/all/"+(x.id)+"\n**Post Link**:  \n"+(message.body_markdown)})
                else:pass
            #open blacklist
            with open('blacklist', 'r') as f:
                blacklist = f.read().split('\n')
            for message in x.messages:
                lowerx2_list = message.body_markdown.lower().split(" ")
            with open('urgent', 'r') as f:
                    urgentid = f.read().split('\n')
            lowerx_list = x.subject.lower().split(" ")
            thankyou_list = ["thank you!"]
            lowerbody = message.body_markdown
            #This part of the code handles urgent messages like doxxing and threats
            if x.id in urgentid:
                dankmemesmods_list = ["dankmemesmods", "DankMemesMods"]
                if "!urgent" in message.body_markdown:
                    if not message.author in dankmemesmods_list:
                        print(message.author)
                        sub.modmail(x.id).reply("The moderator team has been notified and will be here ASAP. Please include links to all relevant information.")
                        sub.modmail(x.id).highlight()
                        requests.post(webhook3, data={"content":"https://i.kym-cdn.com/photos/images/original/000/644/709/d4a.gif \n\n **ALERT!** URGENT MODMAIL! @here https://mod.reddit.com/mail/all/"+(x.id) + "\n\n**Subject:** " + (x.subject) + "\n\n**full message:** " + (message.body_markdown)})
                    else:pass
                else:pass
                
            elif "A /r/dankmemes submission has been removed!" in x.subject:
                print('automod removal')
                for message in x.messages:
                    sub.modmail(x.id).archive()
                    requests.post(webhook1, data={"content":"New automod removal: https://mod.reddit.com/mail/all/"+(x.id)+"\n**Post Link**:  \n"+(message.body_markdown)})
            elif message.body_markdown in mute_list:
                if message.author in reddit.subreddit('dankmemes').moderator():
                    print("found a mute?")
                    sub.modmail(x.id).reply("archiving this, because the user was muted.", author_hidden=False, internal=True)
                    sub.modmail(x.id).archive()
                    print("done!")
                else: print("uhhh>")
            elif userlower in blacklist:
                print("found blacklisted user " + str(x.user))
                try:
                    sub.modmail(x.id).reply("stop messaging us.")
                except: pass
                sub.modmail(x.id).mute()
                sub.modmail(x.id).archive()
                print("done")
            elif "userignore" in userlower:
                print("found blacklisted user " + str(x.user))
                try:
                    sub.modmail(x.id).reply("stop messaging us.")
                except: pass
                sub.modmail(x.id).mute()
                sub.modmail(x.id).archive()
                print("done")
            
            elif x.subject in removal_list:
                print('automod removal')
                for message in x.messages:
                    sub.modmail(x.id).archive()
                    requests.post(webhook1, data={"content":"New automod removal: https://mod.reddit.com/mail/all/"+(x.id)+"\n**Post Link**:  \n"+(message.body_markdown)})
                break
            elif len([i for i in lowerx_list if i in phone_list]) > 0:
                print('phone number')
                sub.modmail(x.id).archive()
                requests.post(webhook1, data={"content":" @here automod has detected a possible phone number being posted. please check it out asap!. https://mod.reddit.com/mail/all/"+(x.id)})
                break
            elif not x.is_highlighted is True and message.is_internal is False:
                    try:
                        if x.last_mod_update > x.last_user_update:
                            time.sleep(0.1)
                            if x.last_mod_update > x.last_user_update:
                                print("archiving to await user reply")
                                x.reply("archiving to await user response", author_hidden=False, internal=True)
                                x.archive()
                                pass
                            else:pass
                    except: pass
            elif message.is_internal is True:
                if message.is_internal is True:
                    permamute_list = ["!permamute"]
                    unban_list = ["!unban"]
                    replyunban_list = ["!unbanwithreply"]
                    report_list = ["!report"]
                    if message.body_markdown in unban_list:
                        if x.user.ban_status["isBanned"] is True:
                            print('unbanning user. give me a second.')
                            sub.banned.remove(x.user)
                            x.reply("User has been unbanned!",author_hidden= False, internal= True)
                            x.reply("Your permanent ban has been revoked.\n\n Your name has a flag next it. This is your FINAL chance. If you do this again, you will be banned permanently.", author_hidden =True, internal=False)
                            subredditUsernotes = Usernotes(reddit=reddit, subreddit=sub)
                            usertonote = str(x.user)
                            permalink = ("https://mod.reddit.com/mail/all/"+x.id)
                            
                            #subredditUsernotes.addUsernote(user=reddit.redditor(usertonote), note="unbanned", thing=permalink, subreddit=sub, warningType="ban")
                            print("usernoted " + str(x.user))
                        else:
                            x.reply("Error! user is either not banned, or something is broken. let sloth know if this user is still banned", author_hidden=False, internal=True)
                            print(x.user)
                            
                    if message.body_markdown in replyunban_list:
                        if x.user.ban_status["isBanned"] is True:
                            print('unbanning user. give me a second.')
                            sub.banned.remove(x.user)
                            x.reply("User has been unbanned!",author_hidden= False, internal= True)
                            x.reply("Your ban has been revoked.\n\n Your name has a tag next to it that lets us know you've been banned before\n\n If you do this again, you might be banned permanently.", author_hidden =True, internal=False)
                            subredditUsernotes = Usernotes(reddit=reddit, subreddit=sub)
                            usertonote = str(x.user)
                            permalink = ("https://mod.reddit.com/mail/all/"+x.id)
                            print(x.user.ban_reason)
                            subredditUsernotes.addUsernote(user=reddit.redditor(usertonote), note="unbanned", thing=permalink, subreddit=sub, warningType="ban")
                            print("usernoted " + str(x.user))
                            x.archive()
                        else:
                            x.reply("Error! user is either not banned, or something is broken. let me know if this user is still banned", author_hidden=False, internal=True)
                            print(x.user)
                    elif message.body_markdown in permamute_list:
                        if not userlower in blacklist:
                            f = open("blacklist", "a")
                            f.write("{} \n".format(userlower))        
                            x.reply("permamuted!",author_hidden= False, internal= True)
                        else:
                            x.reply("Error! user is  already muted", author_hidden=False, internal=True)
                            print(x.user)
                    #automatically report a user to site administration for harassment
                    elif message.body_markdown in report_list:
                        reddit.subreddit('reddit.com').message("Modmail abuse", "Hi!\n\n /u/"+ str(x.user)+ " is abusing our modmail. \n\n here's a link: \n\n https://mod.reddit.com/mail/perma/"+(x.id)+"\n\n this message was generated automatically. contact u/sloth_on_meth for questions")
                        x.reply("reported user to site admins.", author_hidden=False, internal=True)
                        print("reported")

                    else:print(f"nothing to do with{x.id}")
                else:
                pass
    
    except Exception as e: 
        print("Exception occurred! " +str(e) + (x.id))
        


    