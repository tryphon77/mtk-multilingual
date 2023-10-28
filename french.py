# -*- coding: utf-8 -*-

from surface import Surface4bpp
from tools import load_png_8, make_font, make_title_screen, make_magics, write_dialogs_1, write_dialogs_2, write_stage_scene

encoding = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,'!?:0123456789"-…¤$àâéèêîôùûÇçÀÂÉÈÊÎÔÙÛ>œ"""

small_encoding = """tuvw******************** !***************0123456789******ABCDEFGHIJKLMNOPQRSTUVWXYZ"""

def process(buf, symbol_table):
	font = Surface4bpp.load_from_png_8("res/French/Font.png")
	make_font(buf, symbol_table, "Fre", font)

	fg, _ = load_png_8("res/French/TitleFg.png")
	bg, _ = load_png_8("res/English/TitleBg.png")
	title_font, _ = load_png_8("res/English/TitleFont.png")
	make_title_screen(buf, symbol_table, fg, bg, title_font, "Fre")

	magics_surf, _ = load_png_8("res/French/Magic.png")
	make_magics(
		buf,
		symbol_table,
		magics_surf, 
		"Fre", 
		texts=[
			(1, 2, "tuSELECTION MAGIE tu"), 
			(1, 3, "vw                vw"), 
			(2, 15, " PRESSEZ START !  ")
		],
		encoding=small_encoding
	)

	# Stage 1 scene

	write_dialogs_1(
		buf, 
		symbol_table,
		"Fre", 
		0,
		"************************************"
		"************Honmaru: Quoi?        **"
		"************L'école est envahie   **"
		"************de créatures bizarres!**"
		"************************************"

		"************************************"
		"************Talulu: Honmaru! Ces  **"
		"************monstres viennent du  **"
		"************monde magique!        **"
		"************************************"

		"************************************"
		"************Honmaru: Vraiment?    **"
		"************Mais qu'est-ce qu'il  **"
		"************se passe?             **"
		"************************************"

		"************************************"
		"************Talulu: Talu ?…       **"
		"************Wow, c'est très       **"
		"************intéressant!          **"
		"************************************",
		encoding
	)

	# Stage 1 scene
	write_stage_scene(buf, symbol_table, 1, "Fre", ["Chapitre 1", "La Grande Colère", "de Jabao!"], encoding)


	# Meeting Honmaru and Iyona	
	write_dialogs_2(
		buf, 
		symbol_table,
		"Fre",
		0, 
 		"****************************"
 		"**Honmaru: Talulu! Jabao  **"
 		"**te cherchait!           **"
 		"****************************"

 		"****************************"
 		"**Mais il avait l'air     **"
 		"**un peu bizarre…         **"
 		"****************************"

 		"****************************"
 		"**Il n'est pas très fûté  **"
 		"**mais il est fort…       **"
 		"****************************"

 		"****************************"
 		"**Tu devrais faire        **"
 		"**attention!              **"
 		"****************************"

 		"****************************"
 		"**Iyona: Je ne vois pas   **"
 		"**Harako non plus…        **"
 		"****************************"

 		"****************************"
 		"**Je suis inquiète!       **"
 		"**Sois prudent, Talulu!   **"
 		"****************************",
		 encoding
	)

	# Stage 2 introduction

	write_dialogs_1(
		buf, 
		symbol_table,
		"Fre",
		1,																 
		"************************************"
		"************Jabao: Oww!           **"
		"************Qu'est-ce que …?      **"
		"************Où suis-je?           **"
		"************************************"

		"************************************"
		"************Talulu: Jabao! Tu es  **"
		"************redevenu normal!      **"
		"************                      **"
		"************************************"

		"************************************"
		"************Honmaru: Jabao! Que   **"
		"************s'est-il passé? Où    **"
		"************sont tous les autres? **"
		"************************************"

		"************************************"
		"************Jabao: J'ai vu une    **"
		"************lumière étrange, puis **"
		"************plus rien…            **"
		"************************************"

		"************************************"
		"************Boule de Cristal:     **"
		"************Talulu, va enquêter au**"
		"************Pays Magique!         **"
		"************************************"

		"************************************"
		"************Ria: Talulu, prends   **"
		"************ça! Ça te sera utile… **"
		"************                      **"
		"************************************"

 		"************************************"
		"**        Vous avez la magie      **"
		"**        d'invincibilité!        **"                
 		"**                                **"
 		"************************************"

		"************************************"
		"************Talulu: Parfait!      **"
		"************C'est parti!          **"
		"************                      **"
		"************************************",
		encoding
	)

	# Stage 2 scene
	write_stage_scene(buf, symbol_table, 2, "Fre", ["Chapitre 2", "Au Pays Magique!"], encoding)

	# Meeting Ria
	write_dialogs_2(
		buf, 
		symbol_table,
		"Fre",
		1, 
		"****************************"
		"**Ria: Mimola t'attend…   **"
		"**                        **"
		"****************************"

		"****************************"
		"**Où ça? C'est à toi      **"
		"**de le découvrir…        **"
		"****************************"

		"****************************"
		"**À partir d'ici, tu ren- **"
		"**contreras des trous trop**"
		"****************************"

		"****************************"
		"**étroits pour sauter à   **"
		"**travers. Utilise tes    **"
		"****************************"

		"****************************"
		"**ailes pour te faufiler! **"
		"**Bon courage, Talulu!    **"
		"****************************",
		encoding
	)

	# Stage 3 introduction

	write_dialogs_1(
		buf, 
		symbol_table,
		"Fre",
		2,																 
		"************************************"
		"************Mimola: Talulu?       **"
		"************Que fais-tu dans un   **"
		"************endroit pareil?       **"
		"************************************"

		"************************************"
		"************Talulu: Hein? Mimola? **"
		"************Alors, la fille qui   **"
		"************vient de m'attaquer…  **"
		"************************************"

		"************************************"
		"************Mimola: Voyons… Jamais**"
		"************je ne ferais une chose**"
		"************pareille, Talulu!     **"
		"************************************"

		"************************************"
		"************Talulu: ???           **"
		"************C'était une fausse    **"
		"************Mimola?               **"
		"************************************"

		"************************************"
		"************Boule de Cristal:     **"	
		"************Il se passe quelque   **"
		"************chose au Pays des     **"
		"************************************"

		"************************************"
		"************Livres d'Image!       **"
		"************Mimola: Je viens avec **"
		"************toi, Talulu!          **"
		"************************************"

		"************************************"
		"************Mimola: Si les choses **"
		"************tournent mal, appelle **"
		"************moi!                  **"
		"************************************"

		"************************************"
		"************Talulu: D'accord!     **"
		"************Merci, Mimola!        **"
		"************                      **"
		"************************************",
		encoding
	)

	# Stage 3 scene
	write_stage_scene(buf, symbol_table, 3, "Fre", ["Chapitre 3", "Aventure au Pays", "des Livres d'Images!"], encoding)

	# Stage 3 Ijikawa
	write_dialogs_2(
		buf, 
		symbol_table,
		"Fre",
		4, 
		"****************************"
		"**Ijikawa: Ah, Talulu!    **"
		"**Que se passe-t-il ici?  **"
		"****************************"

		"****************************"
		"**Je me suis révéillée    **"
		"**dans cet endroit étrange…$"
		"****************************"

		"****************************"
		"**C'est encore un coup de **"
		"**tes maudits copains!    **"
		"****************************"

		"****************************"
		"**Grrr… Je suis           **"
		"**super en colère!        **"
		"****************************",
		
		encoding
	)

	
	write_dialogs_2(
		buf, 
		symbol_table,
		"Fre",
		5, 
		"****************************"
		"**Papa: Oh? Talulu?       **"
		"**Comment m'as-tu trouvé? **"
		"****************************"

		"****************************"
		"**Le Roi Hohoho vit plus  **"
		"**loin. Il est très fort. **"
		"****************************"

		"****************************"
		"**Après tout, c'est une   **"
		"**de mes créations!       **"
		"****************************"

		"****************************"
		"**Son point faible? Hmmm… **"
		"**Son nez, probablement…  **"
		"****************************",
		encoding
	)

	# Stage 4 Intro		
	write_dialogs_1(
		buf, 
		symbol_table,
		"Fre",
		3,
		"************************************"
		"************Honmaru: Talulu!      **"
		"************Reviens vite dans     **"
		"************notre monde!          **"
		"************************************"

		"************************************"
		"************Talulu: Qu'est-ce qui **"
		"************ne va pas, Honmaru?   **"
		"************                      **"
		"************************************"

		"************************************"
		"************Honmaru: Iyona a      **"
		"************disparu!              **"
		"************                      **"
		"************************************"

		"************************************"
		"************Talulu: Iyona? Oh non!**"
		"************J'arrive tout de suite!$"
		"************Attends-moi, Honmaru! **"
		"************************************"

		"************************************"
		"************Ria: Talulu, voici une**"
		"************nouvelle magie!       **"
		"************                      **"
		"************************************"

 		"************************************"
		"**                                **"                
		"** Vous recevez la tranchemagie!  **"
 		"**                                **"
 		"************************************",
		 encoding
	)
		
	# Stage 4 scene
	write_stage_scene(buf, symbol_table, 4, "Fre", ["Chapitre 4", "Le Sinistre Plan de Raivar!"], encoding)
		
	# Stage 4 Harako

	write_dialogs_1(
		buf, 
		symbol_table, 
		"Fre",
		4,
		"************************************"
		"************Talulu: Harako…?      **"
		"************Ça va?                **"
		"************                      **"
		"************************************"

		"************************************"
		"************Harako: J'ai gagné un **"
		"************prix de pilotage en   **"
		"************hélicoptère…          **"
		"************************************"

		"************************************"
		"************Comment ai-je pu me   **"
		"************crasher? Attends! Je  **"
		"************faisais quoi au juste?**"
		"************************************"

		"************************************"
		"************Honmaru: Tu es rede-  **"
		"************-nu comme avant!      **"
		"************Parfait!              **"
		"************************************"

		"************************************"
		"************Boule de Cristal: Talu,$"
		"************je ressens une présence$"
		"************maléfique par ici…    **"
		"************************************"

 		"************************************"
		"************Harako: C'est cette   **"
		"************présence qui est      **"
		"************derrière tout ça!     **"
 		"************************************"

 		"************************************"
		"************Honmaru: Alors c'est  **"
		"************elle qui détient      **"
		"************Iyona?                **"
 		"************************************"

 		"************************************"
		"************Talulu: J'y vais,     **"
		"************Honmaru!              **"
		"************                      **"
 		"************************************",
		 encoding
	)

	# Stage 4 Niruru
	write_dialogs_2(
		buf, 
		symbol_table, 
		"Fre",
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
		"Fre",
		3, 
		"****************************"
		"**Ooaya: C'est étrange.   **"
		"**Personne ne fait le     **"
		"****************************"

		"****************************"
		"**ménage. Où sont-ils donc**"
		"**tous passés? Hmm…       **"
		"****************************",
		encoding
	)

	# Stage 4 Ending

	write_dialogs_1(
		buf, 
		symbol_table, 
		"Fre",
		5,
 		"************************************"
		"************Honmaru: Je comprends!**"
		"************Tout cela était       **"
		"************l>œuvre de Raivar!    **"
 		"************************************"

 		"************************************"
		"************Harako: Hmm…          **"
		"************Exactement ce que je  **"
		"************pensais!              **"
 		"************************************"

 		"************************************"
		"************Iyona: Talulu! Honmaru!$"
		"************Vous êtes mes héros!  **"
		"************Merci!                **"
 		"************************************"

 		"************************************"
		"************Honmaru: Oh, ce       **"
		"************n'était rien, Iyona…  **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************Mimola: Honmaru a     **"
		"************raison : il n'a rien  **"
		"************fait du tout!         **"
 		"************************************"

 		"$$$$$$$$$$**************************"
		"$$$$$$$$$$**C'est Talulu qui a    **"
		"$$$$$$$$$$**tout fait!            **"
		"$$$$$$$$$$**                      **"
 		"$$$$$$$$$$**************************"

 		"************************************"
		"************Honmaru: Hé bien, euh…**"
		"************Mimola…!              **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************                      **"
		"************Iyona: Ha ha!         **"
		"************                      **"
 		"************************************"

 		"************************************"
		"************                      **"
		"************Talulu: Talu!         **"
		"************                      **"
 		"************************************",
		 encoding
	)
