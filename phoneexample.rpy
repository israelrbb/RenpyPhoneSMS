init -1 python:
    phone_position_x = 0.3
    phone_position_y = 0.5
    phone_position_x = 0.3
    background_position_y = 0.44

transform phone_transform(pXalign=0.5, pYalign=0.5):
    xcenter pXalign
    yalign pYalign

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
    background Transform("phone_background.png", xcenter=0.5,yalign=0.5)
    foreground Transform("phone_foreground.png", xcenter=0.5,yalign=0.5)
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
    background Frame("phone_send_frame.png", 23, 23,23,23)
    padding(20,20)
    xsize 350

style phone_left:
    background Frame("phone_received_frame.png", 23,23,23,23)
    padding(20,20)
    xsize 350


##### Test Script###

label phone_example:

    ### the sms screen takes 3 elements separated by "," ### the character, the message, the list to append to###
    $ sms(kim_sms, "Hello!",kkchats)
    $ sms(kim_sms, "How are you?",kkchats)
    $ sms(mc_sms,"Im doing good and yourself?’",kkchats)
    $ sms(pat_sms ,"Hey I see you are texting Kim!",patchats)
    $ sms(pat_sms,"Tell him I said hi for me {image=images/emoji/wave.png}",patchats)
    $ sms(mc_sms,"Ok then’",patchats)
    $ sms(kim_sms, "Did Paty just text you?.",kkchats)
    ### doing it this way allows us to retain the choice menu###
    menu:
        "Test Menu"
        "Option 1":
            "Yes she did"
            jump phone_example1
            
        "Option 2":
            "No she did not"
            jump phone_example2

label phone_example1:
    $ sms(mc_sms,"Yes she did’",kkchats)
    $ sms(kim_sms, "great!",kkchats)
    call smshide
    jump endexample
label phone_example2:
    $ sms(mc_sms,"No she did not",patchats)
    $ sms(kim_sms, "Liar!",kkchats)
    $ sms(kim_sms, "shes right here with me!",kkchats)
    call smshide
    jump endexample

label endexample:
    mc "Now you seen that you can go between text messages!"
    mc "But you can also call the phone back and see the message history"
    $ recall = True
    show screen contacts
    mc "that concludes this tutorial"


    return

label smshide:
    $renpy.pause()
    hide screen phonesms
    show screen hidephoneapt
    $ persistent.startsms = False
    $ persistent.newconvo = True
    $ new_message = True
    $renpy.pause()
    return


###Create the list for each chat session###
default kkchats = []
default patchats = []
default contactsl = []


####Define your characters name and the image to be used for the contact image and place a "#" in between them ###
define kim_sms = "Kim#dkphone.png"
define pat_sms = "Paty#patphone.png"
define mc_sms = "mc#patphone.png"


#### Parameters that control character image for new message, how the phone appears, and the reply box##
define new_message = True
define persistent.newconvo = True
define persistent.startsms = False

define recall = False

init python:
    class sms:
        def __init__(self, who, what, where):
            who = who.split("#")
            if who[0] in contactsl:                ###this currently does not server any purpose other than adding a user to the list, more to come soon on this
                pass
            else:                             
                contactsl.append(who[0])
            self.who = who[0]
            self.img = who[1]
            self.what = what
            if self.who == "mc":
                where[-1][1][1].append(self.what) 
                renpy.sound.play("audio/ReceiveText.ogg")
            else:
                where.append([self.who,[self.img,[self.what]]])
                renpy.sound.play("audio/SendText.ogg") 
            #renpy.hide_screen("phonesms")  ####not sure if this is needed
            renpy.show_screen("phonesms", where)
            renpy.pause()


screen phonesms(where):
    tag sms
    style_prefix "phoneFrame"
    frame at phone_transform(phone_position_x, phone_position_y):
        if recall:
            textbutton "close" action Hide("phonesms") ### remove from code
        if persistent.newconvo:
            at phone_appear(phone_position_x, phone_position_y)
        hbox:
            xysize(500,20)
            text where[0][0] xalign 0.5 yalign 0.5
        frame style_prefix None:
            background None xysize(490,697)
            ypos .04
            viewport:
                draggable True
                mousewheel True
                yinitial 1.0  
                vbox:
                    for i in where:
                        for iii,ii in enumerate(i[1][1]):
                            if iii == 0:
                                hbox:
                                    xalign 0.0 spacing 0
                                    if new_message:
                                        add where[0][1] yalign 0.0
                                        $new_message = False
                                        $persistent.newconvo = False
                                    frame:
                                        style "phone_left" xoffset
                                        text ii color "#000000"
                            else:
                                hbox:
                                    xalign 1.0 spacing 0
                                    $new_message = True 
                                    frame:
                                        xalign 0.0
                                        style "phone_right"
                                        text ii color "#000000"
        if persistent.startsms:
            frame style_prefix None:
                xysize(500,57) background "#333b"
                ypos .91
                xpos -.02
                textbutton "Send new message" action Jump("testcode", where)


####contactList###
############################
define kimcontact = True
define patcontact = True


screen contacts:
    modal True
    style_prefix "phoneFrame" 
    frame at phone_transform(phone_position_x, phone_position_y):
        textbutton "close" action Hide("contacts")
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
                    $kklast = kkchats[-1][1][1][-1]
                    hbox:
                        xalign .3
                        text kkchats[0][0] size 30    
                    hbox:
                        xalign 0.0 spacing 0
                        add kkchats[0][1] yalign 0.0
                        frame style_prefix None:
                            style "phone_left" 
                            textbutton kklast action Show("phonesms", where = kkchats)
             
                    if patcontact:
                        $patlast = patchats[-1][1][1][-1]
                        hbox:
                            xalign .3
                            text patchats[0][0] size 30    
                        hbox:
                            xalign 0.0 spacing 0
                            add patchats[0][1] yalign 0.0
                            frame style_prefix None:
                                style "phone_left" 
                                textbutton patlast action[Hide("contacts"), Show("phonesms", where = patchats)]
              
screen hidephone:
    modal True
    style_prefix "phoneFrame"
    frame at phone_disappear(phone_position_x, phone_position_y)
    timer 0.1 action [Hide("hidephone"), Show("aptmain")]

screen hidephoneapt:
    modal True
    tag sms
    style_prefix "phoneFrame"
    frame at phone_disappear(phone_position_x, phone_position_y)
    timer 0.1 action Hide("hidephoneapt")
