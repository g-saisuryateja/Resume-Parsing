from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from pdfminer import high_level
import spacy
from spacy.matcher import Matcher
import re
import nltk
import sys
from nltk.corpus import stopwords
class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__()

		self.centralwidget = QWidget()
		self.setCentralWidget(self.centralwidget)

		#Load the UI file
		uic.loadUi("mcd_project.ui",self)
		# Define our widgets
		self.pdf_browse_button=self.findChild(QPushButton, "pdf_browse_btn")
		self.path_label=self.findChild(QLabel,"path_lbl")
		self.title_label=self.findChild(QLabel,"title_lbl")
		self.display_label=self.findChild(QTextBrowser,"display_lbl")
		self.res_label=self.findChild(QLabel,"result_lbl")
		self.edu_button=self.findChild(QPushButton,"edu_btn")
		self.mail_button=self.findChild(QPushButton,"mail_btn")
		self.name_button=self.findChild(QPushButton,"name_btn")
		self.phone_button=self.findChild(QPushButton,"ph_no_btn")
		self.soft_skills_btn=self.findChild(QPushButton,"soft_skills_btn")
		self.tech_skills_btn=self.findChild(QPushButton,"tech_skills_btn")
		self.display_pic=self.findChild(QLabel,"display_pic")
		self.file_data=""
		# Click the Dropdown Box
		self.pdf_browse_button.clicked.connect(self.clicker)
		#self.doc_browse_button.clicked.connect(self.clicker2)
		self.mail_button.clicked.connect(self.mail_button_fcn)#
		self.name_button.clicked.connect(self.name_button_fcn)#
		self.phone_button.clicked.connect(self.phone_button_fcn)#
		self.soft_skills_btn.clicked.connect(self.soft_skills_btn_fcn)#
		self.tech_skills_btn.clicked.connect(self.tech_skills_btn_fcn)
		self.edu_button.clicked.connect(self.edu_button_fcn)#
		# show the app
		self.show()
		self.display_pic.setScaledContents(True)
		self.display_pic.setPixmap(QtGui.QPixmap("resume_parser.png"))
		# nltk.download('stopwords')
		# nltk.download('punkt')
		if self.file_data:
			self.file_data.replace('\t',' ')
			self.file_data.replace('\n', ' ')
		#####################
	def clicker(self):
		#self.path_label.setText("hello")
		# open file dialoug
		fname= QFileDialog.getOpenFileName(self, "Open File", "", "PDF Files (*.pdf)")
		if fname:
			self.path_label.setText(str(fname[0]))
		###
		file_path=fname[0]
		Text = extract_text_from_pdf(file_path)
		print(Text)  # noqa: T001
		self.file_data=Text
		####
	def mail_button_fcn(self):
		self.res_label.setText("You Have choosen: mail Id Details")
		email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)",self.file_data)
		if email:
			try:
				res=email[0].split()[0].strip(';')
				self.display_label.setText(res)
			except IndexError:
				res=None
	def edu_button_fcn(self):
		self.res_label.setText("You Have choosen: Education Details ")
		# load pre-trained model
		nlp = spacy.load('en_core_web_sm')

		# Grad all general stop words
		STOPWORDS = set(stopwords.words('english'))

		# Education Degrees
		EDUCATION = [
			'BE', 'B.E.', 'B.E', 'BS', 'B.S',
			'ME', 'M.E', 'M.E.', 'MS', 'M.S',
			'BTECH', 'B.TECH', 'B. TECH', 'B-TECH', 'M.TECH', 'MTECH',
			'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'INTERMEDIATE', 'BIEAP'
			, 'BIE', 'BACHELOR', 'UNDERGRADUATION', 'SCHOOL', 'ENGINEERING'
		]
		nlp_text=nlp(self.file_data)
		#sentence tokenizer
		nlp_text = [sent.text.strip() for sent in nlp_text.sents]
		edu = {}
		# Extract education degree
		for index, text in enumerate(nlp_text):
			for tex in text.split():
				# Replace all special symbols
				tex = re.sub(r'[?|$|.|!|,]', r'', tex)
				if tex.upper() in EDUCATION and tex not in STOPWORDS:
					edu[tex] = text + nlp_text[index + 1]

		# Extract year
		education = []
		for key in edu.keys():
			if key.upper() not in education:
				education.append(key.upper())
		print(type(education))
		s = ""
		for i in education:
			s = s + i + ","
		self.display_label.setText(s)


	def soft_skills_btn_fcn(self):
		self.res_label.setText("You Have choosen: Soft Skills Details ")

		# removing stop words and implementing word tokenization
		stop_words = set(nltk.corpus.stopwords.words('english'))
		word_tokens = nltk.tokenize.word_tokenize(self.file_data)
		# remove the stop words
		filtered_tokens = [w for w in word_tokens if w not in stop_words]
		# remove the punctuation
		filtered_tokens = [w for w in word_tokens if w.isalpha()]
		# generate bigrams and trigrams (such as artificial intelligence)
		bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
		# Defining Skills
		skills = ['flexibility', 'adaptability', 'emotional intelligence', 'communication skills'
			, 'team player', 'leadership', 'communication', 'time management', 'analytical understanding',
				  'multitasking', 'multi tasking', 'work ethic', 'work ethics', 'determination', 'logical thinking'
			, 'enthusiastic', 'quick decision making', 'decision making', 'patient', 'positive attitude',
				  'critical thinker', 'coherent communicator']
		skillset = []
		# check for one-grams (example: python)
		for token in filtered_tokens:
			token = token.lower()
			if token in skills:
				if token not in skillset:
					skillset.append(token)
		# check for bi-grams and tri-grams (example: machine learning)
		for ngram in bigrams_trigrams:
			ngram = ngram.lower()
			if ngram in skills:
				if ngram not in skillset:
					skillset.append(ngram)
		s = ""
		for i in skillset:
			s = s + i + ","
		self.display_label.setText(s)

	def tech_skills_btn_fcn(self):
		self.res_label.setText("You Have choosen: Technical Skills Details ")
		# removing stop words and implementing word tokenization
		stop_words = set(nltk.corpus.stopwords.words('english'))
		word_tokens = nltk.tokenize.word_tokenize(self.file_data)
		# remove the stop words
		filtered_tokens = [w for w in word_tokens if w not in stop_words]
		# remove the punctuation
		filtered_tokens = [w for w in word_tokens if w.isalpha()]
		# generate bigrams and trigrams (such as artificial intelligence)
		bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
		# Defining Skills
		skills = ['machine learning', 'big data', 'python', 'java', 'matlab', 'data structures',
				  'design and analysis of algorithms', 'c', 'c++', 'deep learning', 'artificial intelligence',
				  'html', 'javascript', 'ruby', 'r', 'natural language processing', 'os', 'auto cad', 'vlsi',
				  'embedded systems', 'mechatronics', 'php', 'web designing', 'spark', 'hadoop', 'pig', 'hive',
				  'pattern recognition', 'chip designing', 'cryptography', 'computer architecture', 'robotics',
				  'fluid mechanics', 'computer networks', 'dbms', 'mysql', 'mongodb', 'nosql', 'css', 'scala', 'ros', 'opencv', 'linux']
		skillset = []
		# check for one-grams (example: python)
		for token in filtered_tokens:
			token = token.lower()
			if token in skills:
				if token not in skillset:
					skillset.append(token)
		# check for bi-grams and tri-grams (example: machine learning)
		for ngram in bigrams_trigrams:
			ngram = ngram.lower()
			if ngram in skills:
				if ngram not in skillset:
					skillset.append(ngram)

		s=""
		for i in skillset:
			s=s+i+","
		self.display_label.setText(s)

	def phone_button_fcn(self):
		self.res_label.setText("You Have choosen: Phone Number Details ")
		phone = re.findall(re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'),self.file_data)
		if phone:
			number=''.join(phone[0])
			if len(number)>10:
				res='+'+number
				self.display_label.setText(res)
			else:
				self.display_label.setText(number)
	def name_button_fcn(self):
		self.res_label.setText("You Have choosen: Name Details ")
		########
		# load pre-trained model
		nlp = spacy.load('en_core_web_sm')
		# initialize matcher with a vocab
		matcher = Matcher(nlp.vocab)
		nlp_text = nlp(self.file_data)
		# First name and Last name are always Proper Nouns
		pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
		matcher.add('NAME', [pattern])
		matches = matcher(nlp_text)
		for match_id, start, end in matches:
			span = nlp_text[start:end]
			name=span.text
			break
		self.display_label.setText(span.text)

def extract_text_from_pdf(pdf_path):
	return high_level.extract_text(pdf_path)
# Initialize the App
app=QApplication(sys.argv)
UIWindow=UI()
app.exec_()