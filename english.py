# -*- coding: utf-8 -*-

from surface import Surface4bpp
from tools import load_png_8, make_font, make_title_screen, make_magics, write_dialogs_1, write_dialogs_2, write_stage_scene


encoding = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,'!?:0123456789"-…¤$"""
# ¤ and $ are special chars

small_encoding = """tuvw******************** !***************0123456789******ABCDEFGHIJKLMNOPQRSTUVWXYZ"""

def process(buf, symbol_table):
	font = Surface4bpp.load_from_png_8("res/English/Font.png")
	make_font(buf, symbol_table, "Eng", font)

	fg, _ = load_png_8("res/English/TitleFg.png")
	bg, _ = load_png_8("res/English/TitleBg.png")
	title_font, _ = load_png_8("res/English/TitleFont.png")	
	make_title_screen(buf, symbol_table, fg, bg, title_font, "Eng")

	magics_surf, _ = load_png_8("res/English/magic.png")
	make_magics(buf, symbol_table, magics_surf, "Eng")

	# Stage 1 Introduction
	write_dialogs_1(
		buf, 
		symbol_table, 
		"Eng", 
		0,
		"************************************"
		"************Honmaru: Wh… what!?   **"
		"************The school is full of **"
		"************weird creatures!      **"
		"************************************"

		"************************************"
		"************Taru: Honmaru!        **"
		"************These beings are from **"
		"************the magic realm!      **"
		"************************************"

		"************************************"
		"************Honmaru: really?      **"
		"************What the hell is      **"
		"************going on?             **"
		"************************************"

		"************************************"
		"************Taru: Taru?…          **"
		"************Wow,                  **"
		"************this is interesting!  **"
		"************************************", 
		encoding
	)

	# Stage 1 scene
	write_stage_scene(buf, symbol_table, 1, "Eng", ["Chapter 1:", "Jabao's Great Rage!"], encoding)

	# Meeting Honmaru and Iyona	
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Eng",
		0, 
 		"****************************"
 		"**Honmaru: Taru! Jabao was**"
 		"**looking for you!        **"
 		"****************************"

 		"****************************"
 		"**But he looked a bit     **"
 		"**strange…                **"
 		"****************************"

 		"****************************"
 		"**He isn't very smart but **"
 		"**he's strong!            **"
 		"****************************"

 		"****************************"
 		"**You should be careful!  **"
 		"**                        **"
 		"****************************"

 		"****************************"
 		"**Iyona: Harako isn't     **"
 		"**around either…          **"
 		"****************************"

 		"****************************"
 		"**I'm worried!            **"
 		"**Be careful, Taru!       **"
 		"****************************",
		 encoding
	)

	# Stage 2 introduction
	write_dialogs_1(
		buf, 
		symbol_table,
		"Eng",
		1,
		"************************************"
		"************Jabao: Oww!           **"
		"************What the…?            **"
		"************Where am I?           **"
		"************************************"

		"************************************"
		"************Taru: Jabao!          **"
		"************You're back to normal!**"
		"************                      **"
		"************************************"

		"************************************"
		"************Honmaru: Jabao!       **"
		"************What happened? Where's**"
		"************everybody else?       **"
		"************************************"

		"************************************"
		"************Jabao: I saw a strange**"
		"************light, and then       **"
		"************I don't…              **"
		"************************************"

		"************************************"
		"************Crystal ball: Taru,   **"
		"************go to the Land of     **"
		"************Magic to find clues.  **"
		"************************************"

		"************************************"
		"************Ria: Taru, take this. **"
		"************It might be useful…   **"
		"************                      **"
		"************************************"

 		"************************************"
		"**        You got invincibility   **"
		"**        magic!                  **"                
 		"**                                **"
 		"************************************"

		"************************************"
		"************Taru: All right!      **"
		"************Let's go!             **"
		"************                      **"
		"************************************",
		encoding
	)

	# Stage 2 scene
	write_stage_scene(buf, symbol_table, 2, "Eng", ["Chapter 2:", "To the Land of Magic!"], encoding)

	# Meeting Ria
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Eng",
		1, 
		"****************************"
		"**Ria: Mimora is waiting  **"
		"**for you…                **"
		"****************************"

		"****************************"
		"**Where, you ask? That,   **"
		"**you'll have to find out.**"
		"****************************"

		"****************************"
		"**From this point, you'll **"
		"**find narrow holes you   **"
		"****************************"

		"****************************"
		"**can't jump through. So  **"
		"**use your wings and slip **"
		"****************************"

		"****************************"
		"**through them!           **"
		"**Do your best, Taru!     **"
		"****************************",
		encoding
	)

	# Stage 3 introduction
	write_dialogs_1(
		buf, 
		symbol_table, 
		"Eng",
		2,
		"************************************"
		"************Mimora: Taru!         **"
		"************What are you doing in **"
		"************a place like this?    **"
		"************************************"

		"************************************"
		"************Taru: Huh? Mimora?    **"
		"************Then, that girl just  **"
		"************now…! Who…?           **"
		"************************************"

		"************************************"
		"************Mimora: I would never **"
		"************do something like that**"
		"************ to you, Taru!        **"
		"************************************"

		"************************************"
		"************Taru: ???             **"
		"************A fake Mimora?        **"
		"************                      **"
		"************************************"

		"************************************"
		"************Crystal ball: Taru,   **"	
		"************now the Land of Picture¤"
		"************Books seems suspicious!¤"
		"************************************"

		"************************************"
		"************Mimora: I'll go       **"
		"************with you!             **"
		"************                      **"
		"************************************"

		"************************************"
		"************Mimora: When things   **"
		"************get dangerous,        **"
		"************give me a call!       **"
		"************************************"

		"************************************"
		"************Taru: OK!             **"
		"************Thanks, Mimora!       **"
		"************                      **"
		"************************************",
		encoding
	)

	# Stage 3 scene
	write_stage_scene(buf, symbol_table, 3, "Eng", ["Chapter 3:", "A Big Adventure in", "the Land of Picture Books!!"], encoding)

	# Stage 3 Ijikawa
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Eng",
		4, 
		"****************************"
		"**Ijikawa: Ah, Taru! What **"
		"**the heck is going on?   **"
		"****************************"

		"****************************"
		"**When I woke up, I was   **"
		"**in this strange place…  **"
		"****************************"

		"****************************"
		"**It must be the work     **"
		"**of your friends again!  **"
		"****************************"

		"****************************"
		"**Grrr…                   **"
		"**I'm so angry!           **"
		"****************************",
		encoding
	)

	# Meeting Dad
	write_dialogs_2(
		buf, 
		symbol_table,
		"Eng",
		5, 
		"****************************"
		"**Dad: Uh? Taru, how did  **"
		"**you find this place?    **"
		"****************************"

		"****************************"
		"**King Gwahaha lies up    **"
		"**ahead. He's quite strong.$"
		"****************************"

		"****************************"
		"**After all, he's a       **"
		"**character from my book! **"
		"****************************"

		"****************************"
		"**His weak point? Hmmm…   **"
		"**His nose, probably…     **"
		"****************************",
		encoding
	)

	# Stage 4 Intro		
	write_dialogs_1(
		buf, 
		symbol_table, 
		"Eng",
		3,
		"************************************"
		"************Honmaru: Taru!        **"
		"************Hurry up and get back **"
		"************to this world!        **"
		"************************************"

		"************************************"
		"************Taru: What's wrong,   **"
		"************Honmaru?              **"
		"************                      **"
		"************************************"

		"************************************"
		"************Honmaru: Iyona has    **"
		"************disappeared!!         **"
		"************                      **"
		"************************************"

		"************************************"
		"************Taru: Iyona? Oh no!   **"
		"************I'm going back now.   **"
		"************Wait for me, Honmaru! **"
		"************************************"

		"************************************"
		"************Ria: Taru,            **"
		"************I'll give you         **"
		"************some new magic.       **"
		"************************************"

 		"************************************"
		"**                                **"                
		"**     You got halving magic!     **"
 		"**                                **"
 		"************************************",
		 encoding
	)

		
	# Stage 4 scene
	write_stage_scene(buf, symbol_table, 4, "Eng", ["Chapter 4:", "Raivar's Sinister Plan!!"], encoding)
		
	# Stage 4 Harako
	write_dialogs_1(
		buf, 
		symbol_table,
		"Eng",
		4,
		"************************************"
		"************Taru: Harako…?        **"
		"************Are you OK?           **"
		"************                      **"
		"************************************"

		"************************************"
		"************Harako: I've won a    **"
		"************world helicopter      **"
		"************piloting tournament…  **"
		"************************************"

		"************************************"
		"************How could I crash?…   **"
		"************Wait! What the heck   **"
		"************was I doing?          **"
		"************************************"

		"************************************"
		"************Honmaru: You're back  **"
		"************to your old self!     **"
		"************All right!            **"
		"************************************"

		"************************************"
		"************Crystal ball: Taru,   **"
		"************there's an evil       **"
		"************presence here…        **"
		"************************************"

 		"************************************"
		"************Harako: That's what's **"
		"************behind all of this!   **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Honmaru: Then that's  **"
		"************what has Iyona?       **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Taru: I'm going,      **"
		"************Honmaru!!             **"
		"************                      **"
 		"************************************",
		 encoding
	)

	# Stage 4 Niruru
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Eng",
		6, 
		"****************************"
		"**Niruru: Nii!            **"
		"**                        **"
		"****************************",
		encoding
	)
		
	# Stage 4 Ooaya
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Eng",
		3, 
		"****************************"
		"**Ooaya:That's strange.   **"
		"**Everybody skipped       **"
		"****************************"

		"****************************"
		"**cleaning. Where exactly **"
		"**did they go? Hmm…       **"
		"****************************",
		encoding
	)

	# Stage 4 Ending
	write_dialogs_1(
		buf, 
		symbol_table, 
		"Eng",
		5,
 		"************************************"
		"************Honmaru: Now I see!   **"
		"************It was all Raivar's   **"
		"************doing!                **"
 		"************************************"

 		"************************************"
		"************Harako: Hmm…          **"
		"************Just as I thought!    **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Iyona: Taru! Honmaru! **"
		"************Thank you for         **"
		"************saving me!            **"
 		"************************************"

 		"************************************"
		"************Honmaru: Oh, it was   **"
		"************nothing, Iyona…       **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Mimora: Honmaru has   **"
		"************nothing to be bashful **"
		"************about.                **"
 		"************************************"

 		"************************************"
		"************                      **"
		"************Taru did everything!  **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Honmaru: Well, uh…    **"
		"************Mimora…!              **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************                      **"
		"************Iyona: Hee hee.       **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************                      **"
		"************Taru: Yeah!           **"
		"************                      **"
 		"************************************",
		encoding
	)
