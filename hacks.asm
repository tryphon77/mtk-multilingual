ENG equ 1
JAP equ 2
FRE equ 3

load_nemesis_gfx equ 0x1652
loadNemesisGfx equ 0x1652
VDP_reg_01 equ 0xfffd54
VDP_data_port equ 0xc00000
destVpos equ 0xfff81e
enableAndWaitVInt equ 0x14f0
getGfxBankPtrnId equ 0x6cb28
enableSelectMapCheat equ 0xfffd2a
drawText equ 0x156e
selectedMap equ 0xfffd2a
selectedLanguage equ 0xfffd64
mapCheatEnabled equ 0xfffd31
fontVPos equ 0xfff81c
titleScreenJapTiles equ 0x2c836
frameTimer equ 0xfff805


	org 0x12b2 ; auto-enable map cheat and language selection
	jmp shunt12b2
	
	org 0x1968
	jmp shunt1968

	org 0x1740 ; PUSH START BUTTON title screen
	jmp shunt1740

	org 0x1a8c
	jmp shunt1a8c
	
	org 0xb066
	jmp shuntb066 ; languages submenu

	org 0xb094
	jmp shuntb094

	org 0xb1a0
	jmp shuntb1a0
	
	org 0xb1c2
	jmp shuntb1c2 ; language cursor
	
	org 0xb440
	dc.l noMapSelected
		
	org 0xb94a
	jmp shuntb94a ; option screen
	
	org 0xb99c
	jmp shuntb99c ; language menu

	org 0xc4e0
	jmp shuntc4e0
	
	org 0xc50c
	jmp shuntc50c

;	org 0xc516
;	jmp shuntc516

	org 0xc5ac
	jmp shuntc5ac	
	
	org 0xc698
	jmp shuntc698
	
	org 0xf70c ; stage 1 
	jmp shuntf70c
	
	org 0xf72c
	jmp shuntf72c
	
	org 0xfa6c ; PUSH START BUTTON from magics menu
	jmp shuntfa6c
	
	org 0x12758 ; magics
	jmp shunt12758
	
	org 0x12a8c
	jmp shunt12a8c ; NO MAGIC
	
	org 0x1311e
	jmp shunt1311e

	org 0x13172
	jmp shunt13172

	org 0x12e4c
	jmp shunt12e4c

	org 0x6c7a0
	jsr shuntf124
	
	org 0x6c970
	jmp shunt6c970
	
	org 0x14f44 ; staff roll
	jmp shunt14f44
	
	
	org 0x98000

shunt12b2:
	bset.b #6, (mapCheatEnabled)
	tst.w (selectedLanguage)
	bne .exit12b2
	move.w #1, (selectedLanguage)
.exit12b2:
	rts

shunt1740:
	btst.b #4, (frameTimer)
	bne shunt1740Spaces
	
	lea (0x175c), a6
	cmp.w #FRE, (selectedLanguage)
	bne shunt1740Next

	lea (txtPushStartButtonTitle), a6
	bra shunt1740Next

shunt1740Spaces:
	lea (0x1772), a6
	cmp.w #FRE, (selectedLanguage)
	bne shunt1740Next
	
	lea (txtPushStartButtonSpacesTitle), a6

shunt1740Next:
	jsr drawText
	rts

txtPushStartButtonTitle:
	dc.l 0x491c0003
	dc.b "PRESSEZ START", 0
	
txtPushStartButtonSpacesTitle:
	dc.l 0x491c0003
	dc.b "             ", 0
	

shunt1968:
	cmp.w #1, (selectedLanguage)
	beq shunt1968eng
	cmp.w #2, (selectedLanguage)
	beq shunt1968jap
	bra shunt1968fra

shunt1968eng:
	lea (titleScreenTilesEng), a0
	moveq #0, d0
	move.w #nbTitlePtrnsEng, d1
	jsr loadTiles
	move.w #titleFontVPos, (fontVPos)
	lea (0xff5bf0).l, a1
	lea (titleScreenTileMapFgEng), a0
	jsr loadTileMap
	
	jmp 0x198c

shunt1968fra:
	lea (titleScreenTilesFre), a0
	moveq #0, d0
	move.w #nbTitlePtrnsFre, d1
	jsr loadTiles
	move.w #titleFontVPos, (fontVPos)
	lea (0xff5bf0).l, a1
	lea (titleScreenTileMapFgFre), a0
	jsr loadTileMap
	
	jmp 0x198c
shunt1968jap:
	move.w #0xa0, fontVPos
	jmp 0x1970


shunt1a8c:
	cmp.w #2, (selectedLanguage)
	beq shunt1a8cjap
	
	lea (titleScreenTileMapBgEng), a0
	cmp.w #ENG, (selectedLanguage)
	beq shunt1a8cNext
	
	lea (titleScreenTileMapBgFre), a0

shunt1a8cNext:
	jsr loadTileMap
	jmp 0x1aa0

shunt1a8cjap:
	lea (0x3062c).l, a0
	jmp 0x1a92


shuntb94a:
	cmp.w #JAP, (selectedLanguage)
	beq shuntb94aJap
	
	lea (titleScreenTilesEng), a0
	cmp.w #ENG, (selectedLanguage)
	beq shuntb94aNext
	lea (titleScreenTilesFre), a0
	
shuntb94aNext:
	moveq #0, d0
	move.w #nbTitlePtrnsEng, d1
	jsr loadTiles
	move.w #titleFontVPos, (0xfff81c)
	
	jmp 0xb95e

shuntb94aJap:
	lea (titleScreenJapTiles), a0
	jmp 0xb950


; =============================================
shuntc4e0:
	cmp.w #2, (selectedLanguage)
	beq shuntc4e0jap

	cmp.w #3, (selectedLanguage)
	bne shuntc4e0Eng
	lea (table_c71aFre).l, a0
	bra shuntc4e0next

shuntc4e0Eng:
	lea (table_c71aEng).l, a0

shuntc4e0next:
	movea.l (a0, d0), a0
	movea.l (0xfff820), a1
	moveq #0, d0
	jsr loadTileMap
	jmp 0xc4f8

shuntc4e0jap:
	lea (0xc71a), a0
	jmp 0xc4e6


; =============================================
table_c71aEng:
	dc.l data4c48eEng
	dc.l data4c552Eng
	dc.l data4c552Eng
	dc.l data4c5fcEng
	dc.l data4c646Eng
	dc.l data4c6caEng
	dc.l data4c754Eng

table_c736Eng:
	dc.w datasize4c48eEng
	dc.w datasize4c552Eng
	dc.w datasize4c552Eng
	dc.w datasize4c5fcEng
	dc.w datasize4c646Eng
	dc.w datasize4c6caEng
	dc.w datasize4c754Eng

table_c71aFre
	dc.l data4c48eFre
	dc.l data4c552Fre
	dc.l data4c552Fre
	dc.l data4c5fcFre
	dc.l data4c646Fre
	dc.l data4c6caFre
	dc.l data4c754Fre

table_c736Fre
	dc.w datasize4c48eFre
	dc.w datasize4c552Fre
	dc.w datasize4c552Fre
	dc.w datasize4c5fcFre
	dc.w datasize4c646Fre
	dc.w datasize4c6caFre
	dc.w datasize4c754Fre

; =============================================
shuntc50c:
	cmp #2, (selectedLanguage)
	beq shuntc50cjap

	move.w (destVpos), d0
	add.w #0x440, d0
	move.w #0x190, d7
	jsr 0x1652

	cmp #3, (selectedLanguage)
	bne shuntc50cEng

	lea (fontFre), a0
	move.w #fontSizeFre, d1
	bra shuntc50cNext

shuntc50cEng
	lea (fontEng), a0
	move.w #fontSizeEng, d1

shuntc50cNext
	jsr loadTiles
	
	lea (data4c2d2).l, a0
	movea.l (0xfff820), a1
	jsr loadTileMap
	jmp 0xc52a

shuntc50cjap:
	move.w #0x190, d7
	jsr loadNemesisGfx
	jmp 0xc516




; =============================================
shuntc5ac:
	cmp.w #2, (selectedLanguage)
	beq shuntc5acjap
	
	movem.l d0, -(sp)

	;c5e2
	movea.l 0x48(a0), a1
	move.w 0(a1, d7), d0
	bmi	ht
	
	asl.w #3, d0
	movea.l 0x40(a0), a1
	adda d0, a1
	
	jmp 0xc5b2

ht:
	andi.w #0x7fff, d0
	asl.w #2, d0
	movea.l 0x40(a0), a1
	adda d0, a1
	
	movem.l (sp)+, d0
	bsr fun_c5f4
	
	addq.w #2, 0x16(a0)
	sub.l #0x7e0000, d0
	movem.l d0, -(sp)

	movea.l 0x48(a0), a1
	move.w 2(a1, d7), d0

	andi.w #0x7fff, d0
	asl.w #2, d0
	movea.l 0x40(a0), a1
	adda d0, a1
	movem.l (sp)+, d0
	bsr fun_c5f4
	
	jmp 0xc5b8

shuntc5acjap:
	movem.l d0, -(sp)
	jsr 0xc5e2
	movem.l (sp)+, d0
	jmp 0xc5b6


shuntc698:
	cmp #2, (selectedLanguage)
	beq shuntc698jap
	cmp #3, (selectedLanguage)
	bne shuntc698eng

	lea (table_c736Fre), a1
	jmp 0xc69e

shuntc698eng:
	lea (table_c736Eng), a1
	jmp 0xc69e
	
shuntc698jap:
	lea (0xc736), a1
	move.w (a0), d1
	jmp 0xc69e


; =============================================
fun_c5f4:
	;c5f4
	lea (VDP_data_port).l, a2
	move.l d0, 4(a2)
	move.w (a1)+, d2
	move.w d2, (a2)
	add.l #0x800000, d0
	move.l d0, 4(a2)
	move.w (a1), d2
	move.w d2, (a2)
	rts	

shuntf70c:
	cmp.w #JAP, (selectedLanguage)
	beq shuntf70cJap
	
	move.w #0x190, d7
	jsr 0x1652

	move.w #0x0460, d0
	lea (fontEng), a0
	move.w #fontSizeEng, d1
	cmp.w #ENG, (selectedLanguage)
	beq shuntf70cEng

	lea (fontFre), a0
	move.w #fontSizeFre, d1
	
shuntf70cEng:
	jsr loadTiles	
	jmp 0xf716

shuntf70cJap:
	move.w #0x190, d7
	jsr loadNemesisGfx
	jmp 0xf716
	
shuntf72c:
	cmp.w #JAP, (selectedLanguage)
	beq shuntf72cJap

	lea (stage_introsEng), a0
	cmp.w #ENG, (selectedLanguage)
	beq shuntf72cEng

	lea (stage_introsFre), a0

shuntf72cEng:
	movea.l 0(a0, d0), a0
	move.w (sp)+, d0
	lsr.w #5, d0
	ori.w #0x8000, d0
	jsr loadTileMap
	lea (0xff5bf0), a6
	moveq #0, d6
	moveq #0, d7
	move.b (a6)+, d7
	move.b (a6)+, d6
	move.l (a6)+, d5
	jmp 0xf754

shuntf72cJap:
	lea (0xf848), a0
	jmp 0xf732

stage_introsEng:
	dc.l dataf858Eng
	dc.l dataf8beEng
	dc.l dataf922Eng
	dc.l dataf980Eng

stage_introsFre:
	dc.l dataf858Fre
	dc.l dataf8beFre
	dc.l dataf922Fre
	dc.l dataf980Fre

shunt1311e:
	cmp.w #JAP, (selectedLanguage)
	beq shunt1311eJap
	
	move.w #0x2a00, d0

	lea (fontEng), a0
	move.w #fontSizeEng, d1
	
	cmp.w #ENG, (selectedLanguage)
	beq shunt1311eEng
	
	lea (fontFre), a0
	move.w #fontSizeFre, d1
	
shunt1311eEng:
	jsr loadTiles

shunt1311eJap:
	move.w #0x198, d7
	jsr load_nemesis_gfx
	jmp 0x13128


shunt13172:
	cmp.w #JAP, (selectedLanguage)
	beq shunt13172Jap
	
	lea (data1330aEng).l, a0
	cmp.w #ENG, (selectedLanguage)
	beq shunt13172Eng
	
	lea (data1330aFre), a0
shunt13172Eng:	
	movea.l 0(a0, d0), a0
	movea.l (0xfff820).l, a1
	move.l a1, 6(a5)
	moveq #0, d0
	jsr loadTileMap

	lea (data133f2).l, a0
	movea.l (0xfff820).l, a1
	move.l a1, 0xe(a5)
	moveq #0, d0
	jsr loadTileMap

	jmp 0x131a6
	
shunt13172Jap:
	lea (0x1330a), a0
	jmp 0x13178

data1330aEng:
	dc.l data137bcEng
	dc.l data138c0Eng
	dc.l data13aa6Eng
	dc.l data13c94Eng
	dc.l data13df4Eng
	dc.l data13ff0Eng

data1330aFre:
	dc.l data137bcFre
	dc.l data138c0Fre
	dc.l data13aa6Fre
	dc.l data13c94Fre
	dc.l data13df4Fre
	dc.l data13ff0Fre

shunt12e4c:
	movem.l d0, -(sp)
	
	; 12f92
	movea.l	(6, a5), a1
	move.w 0(a1, d7), d0
	bmi half_tile
    asl.w #3, d0
    movea.l 0xe(a5), a1
    adda.w d0, a1

	movem.l (sp)+, d0
	
	; 12fa4
	lea (VDP_data_port).l, a2
    move.l d0, 4(a2)
    move.l (a1), d2
    move.l d2, (a2)
    add.l  #0x800000, d0
    move.l d0, 4(a2)
    move.l 4(a1), d2
    move.l d2, (a2)
	
	jmp 0x12e5c

half_tile:
	andi.w	#0x7fff, d0
    asl.w #2, d0
    movea.l 0xe(a5), a1
    adda.w d0, a1

	movem.l (sp)+, d0
	
	; 12fa4
	lea (VDP_data_port).l, a2
    move.l d0, 4(a2)
    move.w (a1), d2
    move.w d2, (a2)
    add.l  #0x800000, d0
    move.l d0, 4(a2)
    move.w 2(a1), d2
    move.w d2, (a2)
	sub.l #0x7e0000, d0

	movem.l d0, -(sp)
	
	movea.l	(6, a5), a1
	move.w 2(a1, d7), d0

	andi.w	#0x7fff, d0
    asl.w #2, d0
    movea.l 0xe(a5), a1
    adda.w d0, a1

	movem.l (sp)+, d0
	
	; 12fa4
	lea (VDP_data_port).l, a2
    move.l d0, 4(a2)
    move.w (a1), d2
    move.w d2, (a2)
    add.l  #0x800000, d0
    move.l d0, 4(a2)
    move.w 2(a1), d2
    move.w d2, (a2)

	addq.w #2, (0xfff804)
	jmp 0x12e5c

loadTiles:
	; d0 = destination vpos
	; a0 = source
	; d1 = number of tiles
	
	lea (0xc00000), a1

	move.w (VDP_reg_01).l, d7
	bset.l #4, d7
    move.w d7, 4(a1)

	; set auto incrémentation to 1
	
	
	; set DMA length
	lsl.w #4, d1
	move.l #0x93009400, d7
	move.w d1, d6
	lsr.w #8, d6
	move.b d6, d7
	swap d7
	move.b d1, d7
	
	move.l d7, 4(a1)
	
	; set DMA address
	move.l a0, d1
	lsr.l #1, d1
	move.l	#0x96009500, d7
	move.b d1, d7
	swap d7
	lsr.w #8, d1
	move.b d1, d7
	
	move.l d7, 4(a1)
	
	swap d1
	move.w #0x9700, d7
	move.b d1, d7
	
	move.w d7, 4(a1)

	; set DMA command
	move.w #0x4000, d7
	move.w d0, d1
	and.w #0x3fff, d0
	or.w d0, d7
	move.w d7, 4(a1)
	
	move #0x0080, d7
	lsr.w #8, d1
	lsr.w #6, d1
	or.w d1, d7
	move.w d7, -(sp)
	move.w (sp)+, 4(a1)
	
	move.w (VDP_reg_01).l, 4(a1)
	rts

loadTileMap:
	move.l a1, d0
	moveq #0, d7
	move.w (a0)+, d7
.loop:
	move.l (a0)+, (a1)+
	dbf d7, .loop	
	movem.l a1, (0xfff820)
	move.l d0, a1
	rts

shunt6c970:
	move.w (destVpos), d0
	
	cmp.w #JAP, (selectedLanguage)
	beq shunt6c970Jap
	
	cmp.w #ENG, (selectedLanguage)
	beq shunt6c970Eng
	
	lea (magicsFreTiles), a0
	moveq #nbMagicsFreTiles, d1
	jsr loadTiles
	moveq #nbMagicsFreTiles, d1
	bra shunt6c970Next
	
shunt6c970Eng:
	lea (magicsEngTiles), a0
	moveq #nbMagicsEngTiles, d1
	jsr loadTiles
	moveq #nbMagicsEngTiles, d1

shunt6c970Next:
	lsl.w #5, d1
	add.w d1, (destVpos)
	jmp 0x6c97a

shunt6c970Jap:
	move.w #0x194, d7
	jsr loadNemesisGfx
	jmp 0x6c97a

shuntf124:
	
	movem.l a0, -(sp)
	jsr enableAndWaitVInt
	move.w (destVpos), -(sp)
	
	cmp.w #JAP, (selectedLanguage)
	beq shuntf124Jap

	jsr getGfxBankPtrnId
	asl.w #5, d0
	
	lea (magicsEngTiles), a0
	moveq #nbMagicsEngTiles, d1
	cmp.w #ENG, (selectedLanguage)
	beq shuntf124Next
	
	lea (magicsFreTiles), a0
	moveq #nbMagicsFreTiles, d1
	
shuntf124Next:
	jsr loadTiles
	
	move.w (sp)+, (destVpos)
	movem.l (sp)+, a0	
	rts

shuntf124Jap:
	jmp 0xf134

shuntfa6c:
	btst.b #4, frameTimer
	bne shuntfa6cSpaces
	
	lea (0xfa88), a6
	cmp.w #FRE, (selectedLanguage)
	bne shuntfa6cNext
	lea (magicPushStartFre), a6
	
shuntfa6cSpaces:
	lea (0xfa9e), a6
	cmp.w #FRE, (selectedLanguage)
	bne shuntfa6cNext
	lea (magicSpacesFre), a6

shuntfa6cNext:	
	jsr drawText
	rts

magicPushStartFre:
	dc.l 0x49960003
	dc.b "PRESSEZ START", 0

magicSpacesFre:
	dc.l 0x49960003
	dc.b "             ", 0

	even
shunt12758:
	cmp.w #JAP, (selectedLanguage)
	beq shunt12758Jap
	
	lea (magicsEngTileMap).l, a0
	cmp.w #ENG, (selectedLanguage)
	beq shunt12758Next
	
	lea (magicsFreTileMap), a0

shunt12758Next	
	move.w #0x8000, d0
	jsr loadTileMap
	jmp 0x12768

shunt12758Jap:
	lea (0x12854), a0
	jmp 0x1275e


shunt12a8c:
	lea (0x12a9a), a6
	cmp.w #FRE, (selectedLanguage)
	bne shunt12a8cNext	
	lea (noMagicFre), a6
shunt12a8cNext:
	jmp 0x12a92

noMagicFre:
	dc.l 0x759a0003
	dc.b "PAS DE MAGIE", 0

	even
shuntb99c:
	lea (txtLanguage), a6
	jsr drawText
	jmp 0xb9a4

shuntb066:
	move.w (selectedLanguage), d0
	asl.w #2, d0
	lea (txtSubLanguages), a0
	movea.l (a0, d0), a6
	jsr drawText
	move.w (selectedMap), d0
	jmp 0xb06e

shuntb1a0:
	movea.l cursorsTextsPtr(pc, d0), a6
	jsr drawText
	rts
	
shuntb1c2:
	movea.l cursorsTextsPtr(pc, d0), a6
	jsr drawText
	rts

	even
cursorsTextsPtr:
	dc.l blankControl 
	dc.l cursorControl ; CONTROLS
	dc.l blankBGM 
	dc.l cursorBGM ; BGM
	dc.l blankSE 
	dc.l cursorSE ; SE
	dc.l blankVOICE 
	dc.l cursorVOICE ; VOICE
	dc.l blankMAP ; MAP
	dc.l cursorMAP ; MAP
	dc.l blankLanguage
	dc.l cursorLanguage
	dc.l blankEXIT ; EXIT
	dc.l cursorEXIT ; EXIT


cursorControl:
	dc.l 0x44120003 
	dc.b ":", 0
	even
blankControl:
	dc.l 0x44120003
	dc.b " ", 0 
	even
	
cursorBGM:
	dc.l 0x46120003
	dc.b ":", 0
	even
blankBGM:
	dc.l 0x46120003 
	dc.b " ", 0 
	even

cursorSE:
	dc.l 0x47120003 
	dc.b ":", 0
	even
blankSE:
	dc.l 0x47120003 
	dc.b " ", 0 
	even

cursorVOICE:
	dc.l 0x48120003 
	dc.b ":", 0
	even
blankVOICE:
	dc.l 0x48120003 
	dc.b " ", 0 
	even

cursorMAP:
	dc.l 0x49120003 
	dc.b ":", 0
	even
blankMAP:
	dc.l 0x49120003 
	dc.b " ", 0 
	even

cursorLanguage:
	dc.l 0x4a120003
	dc.b ":", 0
	even
blankLanguage:
	dc.l 0x4a120003
	dc.b " ", 0
	even

cursorEXIT:
	dc.l 0x4b120003 
	dc.b ":", 0
	even
blankEXIT:
	dc.l 0x4b120003 
	dc.b " ", 0 
	even



shunt14f44:
	lea (titleScreenTilesEng), a0
	move.w #0x0, d0
	move.w #nbTitlePtrnsEng, d1
	jsr loadTiles
	move.w #titleFontVPos, (0xfff81c)
	
	jmp 0x14f58

shuntb094:
	asl.w #4, d0
	lea subMenuCallbacks(pc, d0.w), a1
	jmp 0xb09a

subMenuCallbacks:
	dc.l 0xb246 ; CONTROLS right
	dc.l 0xb25e ; CONTROLS left
	dc.l 0xb0e2 ; CONTROLS A
	dc.l 0xb0e2 ; CONTROLS B, C
	
	dc.l 0xb392 ; BGM right
	dc.l 0xb3ac ; BGM left
	dc.l 0xb34e ; BGM A
	dc.l 0xb362 ; BGM B, C

	dc.l 0xb3d0 ; SE right
	dc.l 0xb3de ; SE left
	dc.l 0xb34e ; SE A
	dc.l 0xb3c2 ; SE B, C

	dc.l 0xb3fa ; VOICE right
	dc.l 0xb408 ; VOICE left
	dc.l 0xb34e ; VOICE A
	dc.l 0xb3ec ; VOICE B, C

	dc.l 0xb416 ; MAP right
	dc.l mapLeftCallback ; 0xb432 ; MAP left
	dc.l 0xb0e2 ; MAP A
	dc.l 0xb0e2 ; MAP B, C

	dc.l languageRightCallback
	dc.l languageLeftCallback
	dc.l languageACallback
	dc.l languageBCallback

	dc.l 0xb0e2 ; EXIT right
	dc.l 0xb0e2 ; EXIT left
	dc.l 0xb000 ; EXIT A
	dc.l 0xb000 ; EXIT B, C

languageRightCallback:
	addq.w #1, (selectedLanguage)
	move.w (selectedLanguage), d0
	asl.w #2, d0
	move.l txtSubLanguages(pc, d0.w), d0
	bne .exit1
	subq.w #1, (selectedLanguage)
.exit1:
	rts

languageLeftCallback:
	subq.w #1, (selectedLanguage)
	bne .exit2
	move.w #1, (selectedLanguage)
.exit2:
	rts

languageACallback:
	rts

languageBCallback:
	rts

mapLeftCallback:
	subq.w #1, (selectedMap)
	bpl .mapLeftCallbackEnd
	move.w #0, (selectedMap)
.mapLeftCallbackEnd:
	rts


txtLanguage:
	dc.l 0x4a160003 ; write at VPOS 0xca16
	dc.b "LANGUAGE", 0
	even

txtSubLanguages:
	dc.l 0
	dc.l txtEnglish
	dc.l txtJapanese
	dc.l txtFrench
	dc.l 0
	even

txtEnglish:
	dc.l 0x4a280003
	dc.b "ENGLISH  ", 0
	even

txtJapanese:
	dc.l 0x4a280003
	dc.b "JAPANESE", 0
	even

txtFrench:
	dc.l 0x4a280003
	dc.b "FRENCH  ", 0
	even

noMapSelected:
	dc.l 0x49280003
	dc.b "NO MAP", 0
	even












