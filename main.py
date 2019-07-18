# encoding=utf-8
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QLabel, QLineEdit,
QTextEdit,QSplitter, QStyleFactory,QGridLayout, QPushButton, QApplication
,QMainWindow, QAction, QFileDialog,QMessageBox)
from PyQt5.QtCore import Qt,QDateTime
from PyQt5.QtGui import QIcon,QPixmap
from PIL import Image,ImageDraw
import pytesseract
import os
import configparser 


class Example(QWidget):
    
	def __init__(self):
		super().__init__()

		self.initUI()
	    
	    
	def initUI(self):
    	#框架
		box = QHBoxLayout(self)

		box_pos = QFrame(self)
		box_pos.setFrameShape(QFrame.StyledPanel)

		box_cut = QFrame(self)
		box_cut.setFrameShape(QFrame.StyledPanel)
		box_cut_show = QFrame(self)
		box_cut_show.setFrameShape(QFrame.StyledPanel)

		box_col = QFrame(self)
		box_col.setFrameShape(QFrame.StyledPanel)
		box_col_show = QFrame(self)
		box_col_show.setFrameShape(QFrame.StyledPanel)

		box_run = QFrame(self)
		box_run.setFrameShape(QFrame.StyledPanel)

		spl_cut = QSplitter(Qt.Horizontal)
		spl_cut.addWidget(box_cut)
		spl_cut.addWidget(box_cut_show)

		spl_col = QSplitter(Qt.Horizontal)
		spl_col.addWidget(box_col)
		spl_col.addWidget(box_col_show)

		spl_all = QSplitter(Qt.Vertical)
		spl_all.addWidget(box_pos)
		spl_all.addWidget(spl_cut)
		spl_all.addWidget(spl_col)
		spl_all.addWidget(box_run)

		box.addWidget(spl_all)

		#添加栅格
		#1 文件夹选择
		grid_pos = QGridLayout()

		self.but_pos = QPushButton('选择文件夹',self)
		grid_pos.addWidget(self.but_pos,0,0,1,1)

		lbl_warn = QLabel('***注意！文件夹里只能有图片***\n***注意！xy只能为整数***')
		lbl_warn.setStyleSheet("color:red")
		grid_pos.addWidget(lbl_warn,1,0,1,1)

		self.lbl_pos = QLabel('<------- *先点这个*',self)
		grid_pos.addWidget(self.lbl_pos,0,1,1,4)

		box_pos.setLayout(grid_pos)

		#2 截图位置
		grid_cut = QGridLayout()

		self.but_save = QPushButton('Save',self)
		grid_cut.addWidget(self.but_save,1,0,1,1)

		self.but_load = QPushButton('Load',self)
		grid_cut.addWidget(self.but_load,2,0,1,1)

		show_rot=QLabel('rotate:')
		grid_cut.addWidget(show_rot,1,1,2,1)

		self.ed_rot = QLineEdit(self)
		grid_cut.addWidget(self.ed_rot,1,2,2,1)
		self.ed_rot.setText(str(rotate))

		show_x1=QLabel('x1:')
		grid_cut.addWidget(show_x1,1,3)

		show_y1=QLabel('y1:')
		grid_cut.addWidget(show_y1,1,5)

		show_x2=QLabel('x2:')
		grid_cut.addWidget(show_x2,2,3)

		show_y2=QLabel('y2:')
		grid_cut.addWidget(show_y2,2,5)

		self.ed_x1 = QLineEdit(self)
		grid_cut.addWidget(self.ed_x1,1,4)
		self.ed_x1.setText(str(x1))

		self.ed_y1 = QLineEdit(self)
		grid_cut.addWidget(self.ed_y1,1,6)
		self.ed_y1.setText(str(y1))

		self.ed_x2 = QLineEdit(self)
		grid_cut.addWidget(self.ed_x2,2,4)
		self.ed_x2.setText(str(x2))

		self.ed_y2 = QLineEdit(self)
		grid_cut.addWidget(self.ed_y2,2,6)
		self.ed_y2.setText(str(y2))

		self.but_view = QPushButton('View ->',self)
		grid_cut.addWidget(self.but_view,1,7,2,1)

		box_cut.setLayout(grid_cut)

		grid_cut_show = QGridLayout()
		self.lbl_cut_show=QLabel(self)
		grid_cut_show.addWidget(self.lbl_cut_show,0,0)
		box_cut_show.setLayout(grid_cut_show)

		#3 截图颜色
		grid_col = QGridLayout()

		show_r=QLabel('r:')
		grid_col.addWidget(show_r,1,1)
		self.ed_r = QLineEdit(self)
		grid_col.addWidget(self.ed_r,1,2)
		self.ed_r.setText(str(r))

		show_g=QLabel('g:')
		grid_col.addWidget(show_g,1,3)
		self.ed_g = QLineEdit(self)
		grid_col.addWidget(self.ed_g,1,4)
		self.ed_g.setText(str(g))

		show_b=QLabel('b:')
		grid_col.addWidget(show_b,1,5)
		self.ed_b = QLineEdit(self)
		grid_col.addWidget(self.ed_b,1,6)
		self.ed_b.setText(str(b))

		box_col.setLayout(grid_col)
		
		grid_col_show = QGridLayout()
		self.lbl_col_show=QLabel(self)
		grid_col_show.addWidget(self.lbl_col_show,0,0)
		box_col_show.setLayout(grid_col_show)

		#4 开始
		gird_run = QGridLayout()

		self.but_run = QPushButton('开工!',self)
		gird_run.addWidget(self.but_run,1,0)

		self.lbl_run_info = QLabel('0. 文件夹里只能存在图片文件，参数只能写数字，开工后不要再点界面，不然会崩溃。重启没法解决就删除‘config.ini’\n1. 准确度约95%，识别不出也很正常，太多识别不出可以改rgb\n2. ‘save’是保存到配置文件，‘load’是从配置文件读取，配置文件不会因关闭软件消失\n3. ‘view’是用当前文本栏的配置查看，不会保存\n4. 工作进度在左上角，工作完后会自动新建一个文件夹，里面的.txt以逗号切分导入excel即可\n5. 更多BUG联系作者，qq：1149580368',self)
		self.lbl_run_info.setStyleSheet("color:blue")
		gird_run.addWidget(self.lbl_run_info,1,1)

		self.lbl_run_res = QLabel('     示例温度:    ℃',self)
		self.lbl_run_res.setStyleSheet("color:red")
		gird_run.addWidget(self.lbl_run_res,1,2)

		box_run.setLayout(gird_run)

		#按钮事件
		#1 选择文件夹
		self.but_pos.clicked.connect(self.folder_posision)
		#2 save写入config.ini
		self.but_save.clicked.connect(self.save_config)
		#3 load载入config.ini
		self.but_load.clicked.connect(self.load_config)
		#4 view查看当前文本栏的效果
		self.but_view.clicked.connect(self.view_change)
		#5 run开工
		self.but_run.clicked.connect(self.run_tmp)

		#大小调整
		self.resize(1000,500)

		#显示
		self.setWindowTitle('批量图像识别 v0.1')
		self.setWindowIcon(QIcon("ico.ico"))
		self.show()

	#事件区
	#1 选择文件夹，导出文件夹内图片，首张图片的裁剪和识别信息
	def folder_posision(self):
		global cur_folder
		cur_folder=QFileDialog.getExistingDirectory(None, "文件夹选择 (只能存在图片这一种类型的文件)", "")
		if cur_folder !='':
			self.lbl_pos.setText(cur_folder)
			global rot,box,col
			tmp=im_show(cur_folder,rotate,box,col)
			self.lbl_cut_show.setPixmap(QPixmap(origin_url+'\cut.png'))
			self.lbl_col_show.setPixmap(QPixmap(origin_url+'\\black.png'))
			self.lbl_run_res.setText('     示例温度: '+tmp+' ℃')
			os.remove(origin_url+'\\black.png')
			os.remove(origin_url+'\cut.png')
	#2 保存到config
	def save_config(self):
		global work_mode,origin_url
		if work_mode==1:
			rotate=self.ed_rot.text()
			x1=self.ed_x1.text()
			y1=self.ed_y1.text()
			x2=self.ed_x2.text()
			y2=self.ed_y2.text()
			r=self.ed_r.text()
			g=self.ed_g.text()
			b=self.ed_b.text()
			global rot,box,col
			rot=rotate
			box=(x1,y1,x2,y2)
			col=(r,g,b)
			config.set("normal", "rotate", str(rotate))
			config.set("normal", "x1", str(x1))
			config.set("normal", "y1", str(y1))
			config.set("normal", "x2", str(x2))
			config.set("normal", "y2", str(y2))
			config.set("normal", "r", str(r))
			config.set("normal", "g", str(g))
			config.set("normal", "b", str(b))
			config.write(open(origin_url+'\config.ini', 'w'))
	#3 载入config
	def load_config(self):
		config = configparser.ConfigParser()
		config.read(origin_url+'\config.ini', encoding="utf-8") 
		conf=config.items('normal')
		rotate=float(conf[0][1])
		x1=int(conf[1][1])
		y1=int(conf[2][1])
		x2=int(conf[3][1])
		y2=int(conf[4][1])
		r=int(conf[5][1])
		g=int(conf[6][1])
		b=int(conf[7][1])
		global rot,box,col
		rot=rotate
		box=(x1,y1,x2,y2)
		col=(r,g,b)
		self.ed_x1.setText(str(x1))
		self.ed_x2.setText(str(x2))
		self.ed_y1.setText(str(y1))
		self.ed_y2.setText(str(y2))
		self.ed_rot.setText(str(rotate))
		self.ed_r.setText(str(r))
		self.ed_g.setText(str(g))
		self.ed_b.setText(str(b))
	#4 预览当前的修改
	def view_change(self):
		global work_mode,origin_url,cur_folder
		if work_mode==1:
			rotate=float(self.ed_rot.text())
			x1=int(self.ed_x1.text())
			y1=int(self.ed_y1.text())
			x2=int(self.ed_x2.text())
			y2=int(self.ed_y2.text())
			r=int(self.ed_r.text())
			g=int(self.ed_g.text())
			b=int(self.ed_b.text())
			cur_box=(x1,y1,x2,y2)
			cur_col=(r,g,b)
			tmp=im_show(cur_folder,rotate,cur_box,cur_col)
			self.lbl_cut_show.setPixmap(QPixmap(origin_url+'\cut.png'))
			self.lbl_col_show.setPixmap(QPixmap(origin_url+'\\black.png'))
			self.lbl_run_res.setText('     示例温度: '+tmp+' ℃')
			os.remove(origin_url+'\\black.png')
			os.remove(origin_url+'\cut.png')
	#5 开工
	def run_tmp(self):
		global work_mode,cur_folder,rot,box,col
		if work_mode==1:
			work_mode=2
			photo = os.listdir()
			number=str(len(photo))
			#当前文件夹名
			folder_name=cur_folder.split('/')[-1]
			#当前目录
			folder_upurl=cur_folder.split(folder_name)[0]
			#当前时间
			now = str(QDateTime.currentDateTime().toSecsSinceEpoch())
			#新建同级文件夹
			new_folder=folder_upurl+folder_name+'_'+now
			os.mkdir(new_folder)
			tmpstr=''
			counter=0
			for im in photo:
				image=Image.open(im)
				#旋转裁剪
				newim=image.rotate(rot)
				newim=newim.crop(box)
				#以原名保存旋转裁剪后图像
				newim.save(new_folder+'\\'+im)
				#获取尺寸
				pix=newim.load()
				width=newim.size[0]
				height=newim.size[1]
				r=col[0]
				g=col[1]
				b=col[2]
				#新建图片，得到黑白转换后的图片：bim
				bim=Image.new('RGB', (width, height), (255, 255, 255))
				draw = ImageDraw.Draw(bim)
				for i in range(width):
					for j in range(height):
						#g & b >240 to black other to white
						if pix[i,j][0]>r and pix[i,j][1]>g and pix[i,j][2]>b:
							draw.point((i, j), fill=(0,0,0))
						else:
							draw.point((i, j), fill=(255,255,255))
				#获取温度
				tmp=pytesseract.image_to_string(bim)
				#写入txt
				tmpstr+=im+','+str(tmp)+'\n'
				counter+=1
				self.setWindowTitle('当前进度: '+str(counter)+'/'+str(number))
			txt=open(new_folder+'\\'+'temperature.txt', mode='w')
			txt.write(tmpstr)
			txt.close()
			work_mode=1
			QMessageBox.question(self, '搞完了，正确率看天命',"赶紧导到excel里，按钮都没用", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

#根据路径返回
#1.裁剪图片
#2.黑化图片
#*3.温度 
def im_show(cur_folder,cur_rot,cur_box,cur_col):
	global work_mode
	os.chdir(cur_folder)
	photo = os.listdir()
	work_mode=1
	#看第一张
	test_photo=photo[0]
	image=Image.open(test_photo)
	#旋转裁剪
	newim=image.rotate(cur_rot)
	newim=newim.crop(cur_box)
	newim.save(origin_url+'\cut.png')
	#黑白变化
	pix=newim.load()
	width=newim.size[0]
	height=newim.size[1]
	r=cur_col[0]
	g=cur_col[1]
	b=cur_col[2]
	bim=Image.new('RGB', (width, height), (255, 255, 255))
	draw = ImageDraw.Draw(bim)
	for i in range(width):
		for j in range(height):
			#g & b >240 to black other to white
			if pix[i,j][0]>r and pix[i,j][1]>g and pix[i,j][2]>b:
				draw.point((i, j), fill=(0,0,0))
			else:
				draw.point((i, j), fill=(255,255,255))
	bim.save(origin_url+'\\black.png')
	#识别
	tmp=pytesseract.image_to_string(bim)
	return tmp
        
if __name__ == '__main__':
    #先检查并创建配置文件config.ini
	config_live='config.ini' in os.listdir()
	config = configparser.ConfigParser()
	if not config_live:
		config['normal'] = {'rotate': '0','x1': '0','y1': '0','x2': '200','y2': '100','r':'0','g':'100','b':'150'}
		config.write(open('config.ini', 'w'))
	config.read('config.ini', encoding="utf-8") 
	conf=config.items('normal')
	#初读信息
	rotate=float(conf[0][1])
	x1=int(conf[1][1])
	y1=int(conf[2][1])
	x2=int(conf[3][1])
	y2=int(conf[4][1])
	r=int(conf[5][1])
	g=int(conf[6][1])
	b=int(conf[7][1])
	global box,col,rot,cur_folder
	rot=rotate
	box=(x1,y1,x2,y2)
	col=(r,g,b)
	cur_folder=''

	#0：初始
	#1：导入文件夹
	#2：正在工作
	global work_mode,origin_url
	work_mode=0
	origin_url=os.getcwd()

	tmp=''

	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
