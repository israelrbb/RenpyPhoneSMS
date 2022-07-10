#############phone and message transitins


init -1 python:
    phone_position_x = 0.3
    phone_position_y = 0.5
    phone_position_x = 0.3
    background_position_y = 0.44

transform phone_transform(pXalign=0.5, pYalign=0.5):
    xcenter pXalign
    yalign pYalign
    on hide:
        yoffset 100
        easein_back 1.5 yoffset 1300

transform phone_appear(pXalign=0.5, pYalign=0.5): #Used only when the dialogue have one element
    xcenter pXalign
    yalign pYalign
    on show:
        yoffset 1080
        easein_back 1.0 yoffset 0
    
transform phone_disappear(pXalign=0.5, pYalign=0.5): 
    xcenter pXalign
    yalign pYalign

    on show:
        yoffset 100
        easein_back 1.5 yoffset 1300

transform message_appear(pDirection):
    alpha 0.0
    xoffset 50 * pDirection
    parallel:
        ease 0.5 alpha 1.0
    parallel:
        easein_back 0.5 xoffset 0

transform message_appear_icon():
    zoom 0.0
    easein_back 0.5 zoom 1.0

style phoneFrame is default
style phoneFrame_frame:
    background Transform("images/phone_background.png", xcenter=0.5,yalign=0.5)
    foreground Transform("images/phone_foreground.png", xcenter=0.5,yalign=0.5)
    ysize 815
    xsize 495

style phoneFrame_viewport:
    yfill True
    xfill True
    yoffset -20

style phoneFrame_vbox:
    spacing 10
    xfill True

style phone_right:
    background Frame("images/phone_send_frame.png", 23, 23,23,23)
    padding(20,20)
    xsize 350

style phone_left:
    background Frame("images/phone_received_frame.png", 23,23,23,23)
    padding(20,20)
    xsize 350

#### Parameters that control character image for new message, how the phone appears, and the reply box##
define persistent.startsms = False  
define pesistent.where = None
define pesistent.who = None


#########
###main part of the code####
##############

init python:
    class contacts:
        def __init__(self, who,img):
            self.who = who
            self.img = img 
            self.list = []

        def sms(self, what, first = False, smshide = True):
            if self.who != "[mcname]":
                pesistent.where = self.list
                pesistent.who = self.who
            self.quien = pesistent.who
            self.where = pesistent.where
            self.first = first
            self.smshide = smshide
            self.what = what
            self.where.append([self.quien,[self.img,[self.what]]])
            renpy.show_screen("phonesms", w = self)
            renpy.pause()
            if smshide:
                renpy.hide_screen("phonesms")

####contactList###
############################
define ksms = contacts("Kim","images/dkphone.png")
define psms = contacts("Paty","images/patphone.png")
define mcsms = contacts("[mcname]","images/momphone.png")
default contactl = [ksms,psms]

screen phonesms(w):
    tag sms
    $ previous_d_who = None
    python:
        yadjValue = float("inf")
        yadj = ui.adjustment()
        yadj.value = yadjValue
    style_prefix "phoneFrame"
    frame at phone_transform(phone_position_x, phone_position_y):
        if w.first:
            at phone_appear(phone_position_x, phone_position_y)
        hbox:
            xysize(500,20)
            text w.where[0][0] xalign 0.5 yalign 0.5
        frame style_prefix None:
            background None xysize(490,697)
            ypos .04
            viewport yadjustment yadj:
                draggable True
                mousewheel True
                #yinitial 1.0  
                vbox:
                    for i in w.where:
                        for ii in i[1][1]:
                            if i[1][0] != "images/momphone.png":
                                hbox:
                                    xalign 0.0 spacing 0
                                    $mms = str(ii)
                                    if previous_d_who != i[1][0]:
                                        if ii == w.what:
                                            add i[1][0] yalign 0.0 at message_appear_icon()
                                        else:
                                            add i[1][0] yalign 0.0
                                    if "mms.png" in mms: 
                                        frame:
                                            style "phone_left" xoffset
                                            imagebutton idle Transform(mms, size=(310, 220), fit="contain") action Show("mmsmessage", i = mms)
                                    else:
                                        frame:
                                            style "phone_left" xoffset
                                            if ii == w.what:
                                                text ii color "#000000" at message_appear(1)  
                                            else:
                                                text ii color "#000000"       
                            else:
                                hbox:
                                    xalign 0.0 spacing 0
                                    $mms = str(ii)
                                    if "mms.png" in mms: 
                                        frame:
                                            style "phone_right" xoffset
                                            imagebutton idle Transform(mms, size=(310, 220), fit="contain") action Show("mmsmessage", i = mms)
                                    else:
                                        frame:
                                            style "phone_right" xoffset
                                            if ii == w.what:
                                                text ii color "#000000" at message_appear(-1)  
                                            else:
                                                text ii color "#000000"
                                        if previous_d_who != i[1][0]:
                                            if ii == w.what:
                                                add i[1][0] yalign 0.0 at message_appear_icon()
                                            else:
                                                add i[1][0] yalign 0.0
                        $ previous_d_who = i[1][0]

        if persistent.startsms:
            $persistent.startsms = False
            frame style_prefix None:
                xysize(500,57) background "#333b"
                ypos .91
                xpos -.02
                $a = str(w.where[0][0])+"test"
                textbutton "Send new message" action Jump(a)
    #########################################################multimediamessage###########################################

screen mmsmessage(i):
    modal True
    frame foreground Transform(i)xalign 0.3 yalign 0.1 
    textbutton "close" action Hide("mmsmessage")


screen smshistory:
    modal True
    style_prefix "phoneFrame" 
    frame at phone_transform(phone_position_x, phone_position_y):
        hbox:
            xysize(500,20)
            text "Contacts" xpos .35 ypos .05
        frame style_prefix None:
            background None xysize(490,697)
            ypos .04
            viewport:
                draggable True
                mousewheel True
                yinitial 1.0
                vbox:
                    for a in contactl:
                        hbox:
                            xalign .3
                            text a.who size 30    
                        hbox:
                            xalign 0.0 spacing 0
                            add a.img yalign 0.0
                            frame style_prefix None:
                                style "phone_left"
                                textbutton a.what action [SetVariable('persistent.startsms', True),Show("phonesms", w = a)]


##### Test Script###

label phone_example:

    mc "Hello"
    mc "Welcome to my phone code"
    mc "Lets get started"
    $renpy.pause(3)
    ### the sms screen takes 3 elements separated by "," ### the character, the message, the list to append to###
    $ ksms.sms("Hello!",True) #the true tells it this is the first message transition the phone in
    $ ksms.sms("How are you?")
    $ mcsms.sms("Im doing good and yourself?’")
    $ psms.sms("Hey I see you are texting Kim!")
    $ psms.sms("Tell him I said hi for me {image=images/emoji/wave.png}")
    $ psms.sms("Ok then’")
    $ ksms.sms("Did Paty just text you?.",False, False) ## we tell it false 1 for its not a new message and the second time so it doesnt hide thge screen if a choice menu is next
    menu:
        "Test Menu"
        "Yes she did":
            "Yes she did"
            jump phone_example1
            
        "No she did not":
            "No she did not"
            jump phone_example2

label phone_example1:
    $ mcsms.sms("Yes she did’")
    $ ksms.sms("great!")
    jump pimages


label phone_example2:
    $ mcsms.sms("No she did not")
    $ ksms.sms("Liar!")
    $ ksms.sms("shes right here with me!")
    $ mcsms.sms("lol sorry, she told me to lie")
    $ ksms.sms("Anyways here is a new feature!")
    jump pimages

label pimages:
    $ ksms.sms("We can now send images that can be clicked on to be expanded")
    $ ksms.sms("bkgndmms.png") ###Selectable image ending in "mms.png"
    mc "Images files automaticlly get converted to imagebuttons and are resized to fit the inside the textbox"
    mc "This way you dont have to worry about resizing"
    mc "The only thing to make sure is that your image ends with 'mms.png' "
    jump endexample

label endexample:
    mc "Now you seen that what this system can do!"
    mc "This next part is still experimetal and I'm still working out some bugs"
    mc "But it allows you to see the text history and start a conversation"
    mc "You can also call the phone back and see the message history"
    mc "select the contact option to bring back the phone"
    call screen smshistory
  
label Kimtest:
    $ mcsms.sms("Hey just testing this new code")
    $ ksms.sms("Hey there!")
    $ mcsms.sms("looks like its working")
    $ ksms.sms("Awesome")
    jump end
label Patytest:
    $ mcsms.sms("Hey just testing this new code")
    $ psms.sms("hey there!")
    $ mcsms.sms("looks like its working")
    $ psms.sms("hey there!")
    jump end

label end:
    mc "That wraps it up for this update"
    mc "Thanks for looking at my code"

    return
