var x_offset = 40
var y_offset = 40
var x_size = 200
var y_size = 200
var game_number = -1
var req

function DisplayO(pnt) {
	ai_row = pnt[0]
	ai_col = pnt[1]
	c = document.getElementById("GameField")
	ctx = c.getContext("2d")
	ctx.beginPath()
	ctx.arc(x_offset+x_size*ai_col + x_size/2, y_offset+y_size*ai_row+y_size/2, y_size/2, 0, 2 * Math.PI)
	ctx.lineWidth = 5
 	ctx.strokeStyle = "blue"
	ctx.stroke()
}

function DisplayX(pnt) {
	ai_row = pnt[0]
	ai_col = pnt[1]
	c = document.getElementById("GameField")
	ctx = c.getContext("2d")
	ctx.beginPath()
	ctx.moveTo(x_offset+x_size*ai_col, y_offset+y_size*ai_row)
	ctx.lineTo(x_offset+x_size*ai_col+x_size, y_offset+y_size*ai_row+y_size)
	ctx.moveTo(x_offset+x_size*ai_col+x_size, y_offset+y_size*ai_row)
	ctx.lineTo(x_offset+x_size*ai_col, y_offset+y_size*ai_row+y_size)
 	ctx.lineWidth = 5
 	ctx.strokeStyle = "red"
	ctx.stroke()
}

function DisplayLine(type, num) {
		c = document.getElementById("GameField")
		ctx = c.getContext("2d")
		if (type == "c") {
			ctx.beginPath()
			ctx.moveTo(x_offset+x_size*num+x_size/2, 0)
			ctx.lineTo(x_offset+x_size*num+x_size/2, y_size*3+2*y_offset)
			ctx.lineWidth = 7
			ctx.strokeStyle = "black"
			ctx.stroke()
		}
		else if (type == "r") {
			ctx.beginPath()
			ctx.moveTo(0, y_offset+y_size*num+y_size/2)
			ctx.lineTo(x_size*3+2*x_offset, y_offset+y_size*num+y_size/2)
			ctx.lineWidth = 7
			ctx.strokeStyle = "black"
			ctx.stroke()
		}
		else if (type == "d" && num == 1) {
			ctx.beginPath()
			ctx.moveTo(0, 0)
			ctx.lineTo(x_size*3+2*x_offset, y_size*3+2*y_offset)
			ctx.lineWidth = 7
			ctx.strokeStyle = "black"
			ctx.stroke()
		}
		else if (type == "d" && num == 2) {
			ctx.beginPath()
			ctx.moveTo(x_size*3+2*x_offset, 0)
			ctx.lineTo(0, y_size*3+2*y_offset)
			ctx.lineWidth = 7
			ctx.strokeStyle = "black"
			ctx.stroke()
		}
}

function handleNextStep() {
	if (req.readyState == 4) {
		elem = document.getElementById("ButtonFirstStepAI")
		if (elem != null)
			document.body.removeChild(elem)

		info = JSON.parse(req.responseText)
		if (Array.isArray(info)) {
			for (i = 0; i < info[1].length; i++) {
				DisplayX(info[1][i])
			}
			for (i = 0; i < info[2].length; i++) {
				DisplayO(info[2][i])
			}
			
			if (info[0] == "AI Win!") {
				res_lbl = document.getElementById('ResultLabel')
				res_lbl.innerHTML = "ИИ выиграл!"
				DisplayLine(info[3], info[4])
				
			}
			if (info[0] == "Human Win!") {
				res_lbl = document.getElementById('ResultLabel')
				res_lbl.innerHTML = "Человек выиграл!"
				DisplayLine(info[3], info[4])
			}
			if (info[0] == "Draw") {
				res_lbl = document.getElementById('ResultLabel')
				res_lbl.innerHTML = "Ничья!"
			}
		}
		else if (info == "Invalid Step!") {
			console.log("Недопустимый ход!")
		}
		else if (info == "Game not founded!") {
			alert("Данная игра - завершена! Начни новую")
		}
		else if (info == "Game not founded!") {
			alert("Данная игра не найдена! Начни новую")
		}
	}
}

function handleCanvasMouseClick(e) {
	c = document.getElementById("GameField")
	ctx = c.getContext("2d")
	rect = c.getBoundingClientRect()
	x_coord = e.clientX - rect.left
	y_coord = e.clientY - rect.top
	
	for (i = 0; i < 3; i++) {
		bound_top = y_offset + i*y_size
		bound_bottom = y_offset + (i+1)*y_size 
		for (j = 0; j < 3; j++) {
			bound_left = x_offset + j*x_size
			bound_right = x_offset + (j+1)*x_size
			if ((bound_left < x_coord) && (x_coord < bound_right) && 
				(bound_top < y_coord) && (y_coord < bound_bottom)) {
				req = new XMLHttpRequest()
				req.onreadystatechange = handleNextStep
				req.open('GET', "/step/" + game_number + "/" + i + j)
				req.send(null)
			}
		}
	}
}

function handleNewGame() {
	if (req.readyState == 4) {
		game_number = JSON.parse(req.responseText)
		elem = document.getElementById("GameField")
		if (elem != null)
			document.body.removeChild(elem)
		elem = document.getElementById("ResultLabel")
		if (elem != null)
			document.body.removeChild(elem)
		elem = document.getElementById("Paragraph")
		if (elem != null)
			document.body.removeChild(elem)
		elem = document.getElementById("ButtonFirstStepAI")
		if (elem != null)
			document.body.removeChild(elem)
			
		// Create BattleField
		cnv = document.createElement("canvas")
		cnv.id = "GameField"
		cnv.width = 3*x_size+2*x_offset
		cnv.height = 3*y_size+2*y_offset
		document.body.appendChild(cnv)
		par = document.createElement("p")
		par.id = "Paragraph"
		document.body.appendChild(par)
		res_lbl = document.createElement("label")
		res_lbl.id = "ResultLabel"
		res_lbl.style.cssText = "color: red; font-size: 32px"
		document.body.appendChild(res_lbl)
		
		// Create Grid
		c = document.getElementById("GameField")
		ctx = c.getContext("2d")
		for (i = 0; i < 3; i++) {
			for (j = 0; j < 3; j++) {
				ctx.rect(x_offset + i*x_size, y_offset + j*y_size, x_size, y_size)
			}
		}
		ctx.lineWidth = 2
		ctx.stroke()
		cnv.addEventListener('click', handleCanvasMouseClick, false)

		// Create Button: "AI first"
		btn_ai_start = document.createElement("button")
		btn_ai_start.id = "ButtonFirstStepAI"
		btn_ai_start.innerHTML = "ИИ ходи первым!"
		btn_ai_start.style.cssText = "color: blue; margin: 4px 2px; cursor: pointer; font-size: 32px "
		btn_ai_start.addEventListener('click', handleButtonFirstStepAI)
		document.body.appendChild(btn_ai_start)
	}
}

function handleButtonStartGame() {
	// Get New Game Number
	req = new XMLHttpRequest()
	req.onreadystatechange = handleNewGame
	req.open('GET', '/start_game')
	req.send(null)
}

function handleButtonFirstStepAI() {
	// First step - AI
	req = new XMLHttpRequest()
	req.onreadystatechange = handleNextStep
	req.open('GET', "/first_step_ai/" + game_number)
	req.send(null)
}
