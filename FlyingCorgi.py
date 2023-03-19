try:
	import pygame, random

	pygame.init()

	# FPS
	fps = pygame.time.Clock()
	FPS = 120

	# Tên game
	pygame.display.set_caption('Flying Corgi')

	#Icon game
	icon = pygame.image.load('Image\icon.jpg')
	pygame.display.set_icon(icon)

	# Font chữ
	pygame.font.init()
	text50 = pygame.font.SysFont('Comic Sans MS', 50)
	text20 = pygame.font.SysFont('lucidaconsole', 40)
	text30 = pygame.font.SysFont('Comic Sans MS', 30)

	# sound
	Gau = pygame.mixer.Sound('Sound\cho_sua.mp3')
	Ang = pygame.mixer.Sound('Sound\cho_ang.mp3')
	Bomp = pygame.mixer.Sound('Sound\boom.mp3')

	# image
	BackGround = pygame.image.load('Image\background.png')
	Corgi = pygame.image.load('Image\corgi.png') # ảnh Corgi trong gameplay
	land = pygame.image.load('Image\land.png') # ảnh nền đất
	ClickToFly = pygame.image.load('Image\clicktofly.png') 
	Mouse = pygame.image.load('Image\mouse.png')
	Boom  = pygame.image.load('Image\boom.png')

	# BackGround
	BACKGROUND_X = 0
	BACKGROUND_Y = 0
	def draw_bg(b1,b2):
		screen.blit(BackGround, (b1, b2))
		screen.blit(BackGround, (b1 + screen_width, b2))

	# Screen
	screen_width = 400	
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height))

	# Color
	Yellow = (250, 250, 0)
	White = (255, 255, 255)
	Black = (0, 0, 0)
	Pink = (250, 150, 200)
	Green = (0, 255, 0)
	Red = (255, 0, 0)
	Blue = (128,255,255)

	# độ cao của 1 lần bay
	jump_step = -4

	# Corgi
	CORGI_X = 100
	CORGI_Y = 250
	Corgi_rect = Corgi.get_rect(center = (CORGI_X, CORGI_Y))
	CORGI_SIZE = 70 # 70x70
	CORGI_STEP_MOVE = jump_step # tốc độ rơi
	CORGI_CORNER = 3 # góc quay của Corgi

	# hàm xoay Corgi
	def rotate_corgi(corgi, step, corner):
		new_corgi = pygame.transform.rotozoom(corgi, - step * corner, 1)
		return new_corgi

	# Land
	LAND_X = 0
	LAND_Y = 500
	LAND_SIZE = (450, 150) # kích cỡ land

	# Trọng lực
	Gravity = 0.17 # càng lớn rơi càng nhanh

	# hàm vẽ land
	def draw_land(l1,l2):
		screen.blit(land, (l1, l2))
		screen.blit(land, (l1 + screen_width, l2))

	# exciter


	# ẩn con trỏ chuột
	pygame.mouse.set_visible(False) 

	# pipe
	top_pipe = pygame.image.load('Image\top_pipe.png')
	bot_pipe = pygame.image.load('Image\bot_pipe.png')
	pipe_list = []
	pipe_high = [240,200,160,120,80,40]
	pipe_distance = 500 # khoảng cách giữa các pipe
	PiwC_index = 0

	# hàm tạo pipe mới
	def creat_pipe():
		random_pipe = random.choice(pipe_high)
		new_top_pipe = top_pipe.get_rect(midbottom = (pipe_distance, random_pipe))
		new_bot_pipe = bot_pipe.get_rect(midtop = (pipe_distance, random_pipe + 150))
		return new_top_pipe, new_bot_pipe

	# hàm di chuyển pipe
	def move_pipe(listpipe):
		for pipe in listpipe:
			pipe.centerx -= 2
		return listpipe

	# hàm vẽ pipe
	def draw_pipe(listpipe):
		for pipe in listpipe:
			if pipe.top <= 0:
				screen.blit(top_pipe, pipe)
			else:
				screen.blit(bot_pipe, pipe)

	# timer _ thời gian vòng lặp tạo pipe mới
	pipe_time = pygame.USEREVENT
	pygame.time.set_timer(pipe_time, 1500)

	# tạo timer để kết thúc sớm âm thanh
	sound_time = pygame.USEREVENT + 1
	pygame.time.set_timer(sound_time, 1000)

	# thời gian chờ sau khi die
	Time_wait = 0

	# Score
	SCORE = 0
	HIGH_SCORE = 0

	# hàm cập nhật
	def update(score, highscore):
		if score > highscore:
			highscore = score
		return highscore

	# hàm khởi tạo
	def reset():
		global CORGI_STEP_MOVE, CORGI_CORNER, LAND_X, LAND_Y, CORGI_Y, SCORE, PiwC_index

		PiwC_index = 0
		CORGI_STEP_MOVE = jump_step
		CORGI_CORNER = 3
		# LAND_X = 0
		# LAND_Y = 500
		Corgi_rect.centery = CORGI_Y
		pipe_list.clear()

	# gameplay
	def gameplay(): # màn hình game play

		running = True # tạo logic đúng để chạy hàm while

		global Gau, Ang, Bomp
		global BACKGROUND_X, BACKGROUND_Y
		global LAND_X, LAND_Y # lấy tọa độ land
		global CORGI_STEP_MOVE # lấy tốc độ rơi
		global CORGI_SIZE # lấy size của corgi
		global CORGI_CORNER # lấy góc quay
		Pipes = pipe_list # lấy list pipe
		global FPS # lấy fps
		global Time_wait # lấy thời gian trễ
		global SCORE, HIGH_SCORE
		global PiwC_index # Pipe index with Corgi _ Cái này để lấy index pipe sau đó so với Corgi_centerx để xác nhận đã vượt 1 pipe -> tăng điểm

		Corgi_rotate = rotate_corgi(Corgi, CORGI_STEP_MOVE, CORGI_CORNER) # tạo hiệu ứng quay cho Corgi

		Gau.play()

		while running: # vòng lặp gameplay
			screen.fill(Blue) # tô màu màn hình

			# Background
			BACKGROUND_X -= 1
			draw_bg(BACKGROUND_X, BACKGROUND_Y)
			if BACKGROUND_X <= - screen_width:
				BACKGROUND_X = 0
			
			mouse_x, mouse_y = pygame.mouse.get_pos() # lấy vị trí chuột
			for event in pygame.event.get(): # bắt sự kiện nhấn phím hoặc nhấn chuột
				if event.type == pygame.QUIT: # nhấn dấu X thì thoát
					running = False
				if event.type == pygame.MOUSEBUTTONDOWN: # sự kiện nhấn chuột
					if Corgi_rect.centery > - jump_step: # tạo điều kiện để Corgi không đi cao quá top màn hình
						CORGI_STEP_MOVE = jump_step # nhảy lên 1 step
				if event.type == pipe_time:
					Pipes.extend(creat_pipe()) # tạo pipe sau 1 khoảng tgian hồi
			
			CORGI_STEP_MOVE += Gravity
			Corgi_rotate = rotate_corgi(Corgi, CORGI_STEP_MOVE, CORGI_CORNER)
			Corgi_rect.centery += CORGI_STEP_MOVE # Corgi di chuyển 
			screen.blit(Corgi_rotate, Corgi_rect)

			# pipe
			Pipes = move_pipe(Pipes)
			draw_pipe(Pipes)

			# score
			text_score = text30.render(str(SCORE), False, Black)
			score_rect = text_score.get_rect(center = (200,50))
			screen.blit(text_score, score_rect)

			# land
			LAND_X -= 1
			draw_land(LAND_X, LAND_Y)
			if LAND_X <= - screen_width:
				LAND_X = 0

			screen.blit(Mouse, (mouse_x, mouse_y)) # hiện con trỏ chuột mới

			# Xử lí va chạm
			for pipe in Pipes:
				if Corgi_rect.colliderect(pipe): # va chạm cột thì game over
					running = False
			if Corgi_rect.centery >= LAND_Y - 35: # corgi chạm đáy thì game over
				running = False 

			# Xử lí nếu vượt qua cột thì tăng điểm
			if not Pipes:
				pass
			else:
				if Corgi_rect.centerx > Pipes[PiwC_index].centerx:
					SCORE += 1
					PiwC_index += 2

			pygame.display.flip()
			fps.tick(FPS)

		# Cập nhật điểm cao
		HIGH_SCORE = update(SCORE, HIGH_SCORE)
		
		Gau.stop()
		Ang.play()

		# vòng lặp màn hình hiện thị điểm sau khi Corgi die
		Quit = False
		running = True
		Bomp_sound = True
		while running: # vòng lặp màn hình hiện thị điểm sau khi Corgi die
			screen.fill(Blue) # tô màu màn hình

			# Background
			draw_bg(BACKGROUND_X, BACKGROUND_Y)
			
			mouse_x, mouse_y = pygame.mouse.get_pos() # lấy vị trí chuột
			for event in pygame.event.get(): # bắt sự kiện nhấn phím hoặc nhấn chuột
				if event.type == pygame.QUIT: # nhấn dấu X thì thoát
					Quit = True
					running = False
				if event.type == pygame.KEYDOWN: # sự kiện bấm phím
					if event.key == pygame.K_SPACE:
						Ang.stop()
						Bomp_sound = False
						Bomp.stop()
						running = False
				if event.type == pipe_time:
					Pipes.extend(creat_pipe()) # tạo pipe sau 1 khoảng tgian hồi
			
			# pipe
			draw_pipe(Pipes)

			# Corgi
			if Corgi_rect.centery < LAND_Y - 35:
				CORGI_STEP_MOVE += Gravity
				Corgi_rotate = rotate_corgi(Corgi, CORGI_STEP_MOVE, CORGI_CORNER)
				Corgi_rect.centery += CORGI_STEP_MOVE
				screen.blit(Corgi_rotate, Corgi_rect)
			else:
				if Bomp_sound:
					Bomp.play()
					for event in pygame.event.get():
						if event.type == sound_time:
							Bomp_sound = False
							Bomp.stop() 

				screen.blit(Boom, (Corgi_rect.centerx - 50, Corgi_rect.centery - 102))
				# rect
				pygame.draw.rect(screen, Black, (110,210,200,200))
				pygame.draw.rect(screen, Black, (97,197,206,206))
				pygame.draw.rect(screen, Yellow, (100,200,200,200))

				# corgi heaven
				Corgi_heaven = pygame.image.load('corgi_heaven.png')
				screen.blit(Corgi_heaven, (230, 100))

				# score
				text_score = text30.render('SCORE: '+str(SCORE), False, Black)
				score_rect = text_score.get_rect(center = (200,270))
				text_high_score = text30.render('BEST: '+str(HIGH_SCORE), False, Black)
				highscore_rect = text_high_score.get_rect(center = (200,340))
				screen.blit(text_score, score_rect)
				screen.blit(text_high_score, highscore_rect)
			
			# land
			draw_land(LAND_X, LAND_Y)
			screen.blit(Mouse, (mouse_x, mouse_y)) # hiện con trỏ chuột mới

			pygame.display.flip()
			fps.tick(FPS)


		pygame.time.wait(Time_wait)
		if Quit:
			pass
		else:
			reset()
			main_game()

	def test(): # hàm dùng để test khi chạy đến 1 giai đoạn bất kì
		print("Passed!")

	# gameover
	def main_game():

		running = True # tạo logic đúng để chạy hàm while
		CheckMouseButton = False # kiểm tra đã nhấn chuột hay chưa

		global LAND_X, LAND_Y # lấy tọa độ land
		global Time_wait, FPS, SCORE, HIGH_SCORE
		global BACKGROUND_X, BACKGROUND_Y

		Quit = False

		while running: # vòng lặp gameplay
			screen.fill(Blue) # tô màu màn hình

			# Background
			BACKGROUND_X -= 1
			draw_bg(BACKGROUND_X, BACKGROUND_Y)
			if BACKGROUND_X <= - screen_width:
				BACKGROUND_X = 0

			mouse_x, mouse_y = pygame.mouse.get_pos() # lấy vị trí chuột
			for event in pygame.event.get(): # bắt sự kiện nhấn phím hoặc nhấn chuột
				if event.type == pygame.QUIT: # nhấn dấu X thì thoát
					Quit = True
					running = False
				if event.type == pygame.MOUSEBUTTONDOWN: # sự kiện nhấn chuột
					if event.button == 1:
						running = False
				if event.type == pipe_time:
					pipe_list.extend(creat_pipe()) # tạo pipe sau 1 khoảng tgian hồi

			screen.blit(ClickToFly, (Corgi_rect.centerx + 10, Corgi_rect.centery - 100))
			screen.blit(Corgi, Corgi_rect)

			# land
			LAND_X -= 1
			draw_land(LAND_X, LAND_Y)
			if LAND_X <= - screen_width:
				LAND_X = 0

			screen.blit(Mouse, (mouse_x, mouse_y)) # hiện con trỏ chuột mới

			pygame.display.flip()
			fps.tick(FPS)

		pygame.time.wait(Time_wait)

		if Quit:
			pass
		else:	
			reset()
			SCORE = 0
			gameplay()

	# Vận hành game
	main_game()
	pygame.quit()
except:
	with Exception as bug:
		print(bug)

input()
