# app.py (Nâng cấp hỗ trợ nhiều khối lớp)

import os
import json
import re
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Lỗi: Không tìm thấy GEMINI_API_KEY. Vui lòng tạo file .env và thêm key vào.")
    exit()

# ==========================================================
# CƠ SỞ DỮ LIỆU CHƯƠNG TRÌNH HỌC TRUNG TÂM (MỚI)
# ==========================================================
# Chứa toàn bộ từ vựng, cấu trúc, trọng âm cho mọi khối lớp.
# Tên của Unit (ví dụ: "Unit 1: All about me!") PHẢI KHỚP
# chính xác với giá trị trong tệp script.js
#
# DỮ LIỆU LỚP 1 ĐÃ ĐƯỢC CẬP NHẬT DỰA TRÊN ẢNH BOOK MAP
# ==========================================================
CURRICULUM_DATA = {
    "1": {
        # === BẮT ĐẦU DỮ LIỆU LỚP 1 (ĐÃ ĐƯỢC CẬP NHẬT) ===
        # Tên Unit được lấy từ script.js
        # Dữ liệu (vocabulary, structures) được lấy từ ảnh Book Map
        "Unit 1: My first day at school": { # Image Unit 1: In the school playground
            "vocabulary": "Phonics: Bb. Vocabulary: ball, bike, book",
            "structures": "Hi, I'm Bill. Bye, Bill.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 2: My school things": { # Image Unit 2: In the dining room
            "vocabulary": "Phonics: Cc. Vocabulary: cake, car, cat, cup",
            "structures": "I have a car.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 3: My toys": { # Image Unit 3: At the street market
            "vocabulary": "Phonics: Aa. Vocabulary: apple, bag, can, hat",
            "structures": "This is my bag.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 4: My body": { # Image Unit 4: In the bedroom
            "vocabulary": "Phonics: Dd. Vocabulary: desk, dog, door, duck",
            "structures": "This is a dog.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 5: My pets": { # Image Unit 5: At the fish and chip shop
            "vocabulary": "Phonics: Ii. Vocabulary: chicken, chips, fish, milk",
            "structures": "I like milk.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 6: My home": { # Image Unit 6: In the classroom
            "vocabulary": "Phonics: Ee. Vocabulary: bell, pen, pencil, red",
            "structures": "It's a red pen.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 7: My family": { # Image Unit 7: In the garden
            "vocabulary": "Phonics: Gg. Vocabulary: garden, gate, girl, goat",
            "structures": "There's a garden.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 8: My clothes": { # Image Unit 8: In the park
            "vocabulary": "Phonics: Hh. Vocabulary: hair, hand, head, horse",
            "structures": "Touch your hair.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 9: My colours": { # Image Unit 9: In the shop
            "vocabulary": "Phonics: Oo. Vocabulary: clocks, locks, mops, pots",
            "structures": "How many clocks? Two.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 10: My hobbies": { # Image Unit 10: At the zoo
            "vocabulary": "Phonics: Mm. Vocabulary: mango, monkey, mother, mouse",
            "structures": "That's a monkey.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 11: My family": { # Image Unit 11: At the bus stop
            "vocabulary": "Phonics: Uu. Vocabulary: bus, run, sun, truck",
            "structures": "She's running. He's running.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 12: My house": { # Image Unit 12: At the lake
            "vocabulary": "Phonics: Ll. Vocabulary: lake, leaf, lemons",
            "structures": "Look at the lemons.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 13: My room": { # Image Unit 13: In the school canteen
            "vocabulary": "Phonics: Nn. Vocabulary: bananas, noodles, nuts",
            "structures": "She's having noodles.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 14: My birthday": { # Image Unit 14: In the toy shop
            "vocabulary": "Phonics: Tt. Vocabulary: teddy bear, tiger, top, turtle",
            "structures": "I can see a tiger.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 15: My activities": { # Image Unit 15: At the football match
            "vocabulary": "Phonics: Ff. Vocabulary: face, father, foot, football",
            "structures": "Point to your hand.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        },
        "Unit 16: My pets": { # Image Unit 16: At home
            "vocabulary": "Phonics: Ww. Vocabulary: wash, water, window",
            "structures": "How many windows can you see? I can see six.",
            "stress": "Không áp dụng",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading'] # ĐÃ THÊM
        }
        # === KẾT THÚC DỮ LIỆU LỚP 1 ===
    },
    "2": {
        # === BẮT ĐẦU DỮ LIỆU LỚP 2 (DỰA TRÊN ẢNH BOOK MAP) ===
        "Unit 1: At my birthday party": {
            "vocabulary": "Phonics: p. Vocabulary: pasta, popcorn, pizza",
            "structures": "The popcorn is yummy.",
            "stress": "Phonics: p",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 2: In the backyard": {
            "vocabulary": "Phonics: k. Vocabulary: kite, bike, kitten",
            "structures": "Is she flying a kite? Yes, she is. / No, she isn't.",
            "stress": "Phonics: k",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 3: At the seaside": {
            "vocabulary": "Phonics: s. Vocabulary: sail, sand, sea",
            "structures": "Let's look at the sea!",
            "stress": "Phonics: s",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 4: In the countryside": {
            "vocabulary": "Phonics: r. Vocabulary: rainbow, river, road",
            "structures": "What can you see? I can see a rainbow.",
            "stress": "Phonics: r",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 5: In the classroom": {
            "vocabulary": "Phonics: q. Vocabulary: question, square, quiz",
            "structures": "What's he doing? He's doing a quiz.",
            "stress": "Phonics: q",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 6: On the farm": {
            "vocabulary": "Phonics: x. Vocabulary: box, fox, ox",
            "structures": "Is there a fox? Yes, there is. / No, there isn't.",
            "stress": "Phonics: x",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 7: In the kitchen": {
            "vocabulary": "Phonics: j. Vocabulary: juice, jelly, jam",
            "structures": "Pass me the jam, please. Here you are.",
            "stress": "Phonics: j",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 8: In the village": {
            "vocabulary": "Phonics: v. Vocabulary: village, van, volleyball",
            "structures": "Can you draw a van? Yes, I can. / No, I can't.",
            "stress": "Phonics: v",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 9: In the grocery store": {
            "vocabulary": "Phonics: y. Vocabulary: yogurt, yams, yo-yos",
            "structures": "What do you want? I want some yams.",
            "stress": "Phonics: y",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 10: At the zoo": {
            "vocabulary": "Phonics: z. Vocabulary: zoo, zebu, zebra",
            "structures": "Do you like the zoo? Yes, I do. / No, I don't.",
            "stress": "Phonics: z",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 11: In the playground": {
            "vocabulary": "Phonics: i. Vocabulary: sliding, riding, driving",
            "structures": "They're driving cars.",
            "stress": "Phonics: i",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 12: At the café": {
            "vocabulary": "Phonics: a. Vocabulary: grapes, cake, table",
            "structures": "The cake is on the table. The grapes are on the table.",
            "stress": "Phonics: a",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 13: In the maths class": {
            "vocabulary": "Phonics: n. Vocabulary: eleven, thirteen, fourteen, fifteen",
            "structures": "What number is it? It's eleven.",
            "stress": "Phonics: n",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 14: At home": {
            "vocabulary": "Phonics: er. Vocabulary: brother, sister, grandmother",
            "structures": "How old is your brother? He's nineteen.",
            "stress": "Phonics: er",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 15: In the clothes shop": {
            "vocabulary": "Phonics: sh. Vocabulary: shirts, shoes, shorts",
            "structures": "Where are the shoes? Over there.",
            "stress": "Phonics: sh",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 16: At the campsite": {
            "vocabulary": "Phonics: t. Vocabulary: tent, teapot, blanket",
            "structures": "Is the blanket near the tent? No, it isn't. It's in the tent.",
            "stress": "Phonics: t",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        }
        # === KẾT THÚC DỮ LIỆU LỚP 2 ===
    },
    "3": {
        # === BẮT ĐẦU DỮ LIỆU LỚP 3 (MỚI TỪ ẢNH) ===
        "Unit 1: Hello": {
            "vocabulary": "bye, fine, goodbye, hello, hi, how, I, thank you, you (Names: Ben, Lucy, Mai, Minh)",
            "structures": "Hello. / Hi. I'm ..., Hello, / Hi, ... I'm ..., Hi. How are you? - Fine, thank you., Goodbye. / Bye.",
            "stress": "Phonics: hello, bye",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 2: Our names": {
            "vocabulary": "how, old, my, name, what, your (Names: Bill, Linh, Mary, Nam)",
            "structures": "What's your name? - My name's ..., How old are you? - I'm ... years old.",
            "stress": "Phonics: Mary, Nam",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 3: Our friends": {
            "vocabulary": "friend, it, Mr, Ms, no, teacher, that, this, yes (Names: Ms Hoa, Mr Long)",
            "structures": "This is ... / That's ..., Is this / that ...? - Yes, it is. / No, it isn't. It's ...",
            "stress": "Phonics: that, thank",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 4: Our bodies": {
            "vocabulary": "ear, eye, face, hair, hand, mouth, nose, open, touch",
            "structures": "What's this? - It's ..., Touch / Open your ...!",
            "stress": "Phonics: hair, ears",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 5: My hobbies": {
            "vocabulary": "cooking, dancing, drawing, painting, running, singing, swimming, walking",
            "structures": "What's your hobby? - It's ..., What's your hobby? - I like ...",
            "stress": "Phonics: painting, running",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 6: Our school": {
            "vocabulary": "art room, classroom, computer room, gym, library, music room, playground, school",
            "structures": "Is this our ...? - Yes, it is. / No, it isn't., Let's go to the ..., OK, let's go.",
            "stress": "Phonics: playground, classroom",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 7: Classroom instructions": {
            "vocabulary": "close, come in, go out, sit down, speak, stand up",
            "structures": "..., please!, May I ...? - Yes, you can. / No, you can't.",
            "stress": "Phonics: speak, stand",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 8: My school things": {
            "vocabulary": "book, eraser, notebook, pen, pencil, pencil case, ruler, school bag",
            "structures": "I have ..., Do you have ...? - Yes, I do. / No, I don't.",
            "stress": "Phonics: book, eraser",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 9: Colours": {
            "vocabulary": "black, blue, brown, colour, green, orange, red, they, white, yellow",
            "structures": "What colour is it? - It's ..., What colour are they? - They're ...",
            "stress": "Phonics: blue, brown",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 10: Break time activities": {
            "vocabulary": "break time, chat, play (badminton, basketball, chess, football, table tennis, volleyball, word puzzles)",
            "structures": "I ... at break time., What do you do at break time? - I ...",
            "stress": "Phonics: football, volleyball",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 11: My family": {
            "vocabulary": "brother, father, mother, sister, sure, numbers from eleven to twenty",
            "structures": "Who's this / that? - It's my ..., How old is he / she? - He's / She's ...",
            "stress": "Phonics: old, sure",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 12: Jobs": {
            "vocabulary": "cook, doctor, driver, farmer, job, nurse, singer, teacher, worker",
            "structures": "What's his / her job? - He's / She's ..., Is he / she ...? - Yes, he / she is. / No, he / she isn't.",
            "stress": "Phonics: mother, doctor",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 13: My house": {
            "vocabulary": "bathroom, bedroom, chair, house, kitchen, lamp, living room, table, here, there, in, on",
            "structures": "Where's the ...? - It's here / there., Where are the ...? - They're ...",
            "stress": "Phonics: house, brown",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 14: My bedroom": {
            "vocabulary": "bed, big, desk, door, new, old, room, small, window",
            "structures": "There's / There are ... in the room., The ... is ... / The ... are ...",
            "stress": "Phonics: room, door",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 15: At the dining table": {
            "vocabulary": "bean, bread, chicken, egg, fish, juice, meat, milk, rice, water",
            "structures": "Would you like some ...? - Yes, please. / No, thanks., What would you like to eat / drink? - I'd like some ..., please.",
            "stress": "Phonics: bread, meat",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 16: My pets": {
            "vocabulary": "bird, cat, dog, goldfish, parrot, rabbit, many, some",
            "structures": "Do you have any ...? - Yes, I do. / No, I don't., How many ... do you have? - I have ...",
            "stress": "Phonics: dog, goldfish",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 17: Our toys": {
            "vocabulary": "bus, car, kite, plane, ship, teddy bear, toy, train, truck",
            "structures": "He / She has ..., They have ...",
            "stress": "Phonics: kite, toy",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 18: Playing and doing": {
            "vocabulary": "dancing, drawing a picture, listening to music, playing basketball, reading, singing, watching TV, writing",
            "structures": "I'm ..., What are you doing? - I'm ...",
            "stress": "Phonics: listen, singing",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 19: Outdoor activities": {
            "vocabulary": "cycling, flying a kite, painting, playing badminton, running, skating, skipping, walking",
            "structures": "He's / She's ..., What's he / she doing? - He's / She's ...",
            "stress": "Phonics: play, fly",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 20: At the zoo": {
            "vocabulary": "climbing, counting, elephant, horse, monkey, peacock, swinging, tiger",
            "structures": "What can you see? - I can see ..., What's the ... doing? - It's ...",
            "stress": "Phonics: parrot, dancing",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        }
        # === KẾT THÚC DỮ LIỆU LỚP 3 ===
    },
    "4": {
        # === BẮT ĐẦU DỮ LIỆU LỚP 4 (MỚI TỪ ẢNH) ===
        "Unit 1: My friends": {
            "vocabulary": "America, Australia, Britain, Japan, Malaysia, Singapore, Thailand, Viet Nam",
            "structures": "Where are you from? - I'm from ..., Where's he / she from? - He's / She's from ...",
            "stress": "Phonics: America, Australia",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 2: Time and daily routines": {
            "vocabulary": "at, fifteen, forty-five, o'clock, thirty, get up, go to bed, go to school, have breakfast",
            "structures": "What time is it? - It's ..., What time do you ...? - I ... at ...",
            "stress": "Phonics: get, bed",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 3: My week": {
            "vocabulary": "Friday, Monday, Saturday, Sunday, Thursday, Tuesday, Wednesday, do housework, listen to music, study at school",
            "structures": "What day is it today? - It's ..., What do you do on ...? - I ...",
            "stress": "Phonics: music, Sunday",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 4: My birthday party": {
            "vocabulary": "April, February, January, March, May, birthday, chips, grapes, jam, juice, lemonade, party, water",
            "structures": "When's your birthday? - It's in ..., What do you want to eat / drink? - I want ...",
            "stress": "Phonics: jam, water",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 5: Things we can do": {
            "vocabulary": "can, cook, draw, play the guitar, play the piano, ride a bike, ride a horse, roller skate, swim, but",
            "structures": "Can you ...? - Yes, I can. / No, I can't., Can he / she ...? - Yes, he / she can. No, he / she can't, but he / she ...",
            "stress": "Phonics: yes, no",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 6: Our school facilities": {
            "vocabulary": "city, mountains, town, village, building, computer room, garden, playground",
            "structures": "Where's your school? - It's in the ..., How many ... are there at your school? - There is / are ...",
            "stress": "Phonics: mountains, villages",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 7: Our timetables": {
            "vocabulary": "art, English, history and geography, maths, music, science, Vietnamese, days of the week (review)",
            "structures": "What subjects do you have today? - I have ..., When do you have ...? - I have it on ...",
            "stress": "Phonics: Vietnamese, science",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 8: My favourite subjects": {
            "vocabulary": "IT, PE, English teacher, painter, maths teacher, because, why",
            "structures": "What's your favourite subject? - It's ..., Why do you like ...? - Because I want to be ...",
            "stress": "Phonics: like, write",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 9: Our sports day": {
            "vocabulary": "December, June, July, November, October, September, sports day",
            "structures": "Is your sports day in ...? - Yes, it is. / No, it isn't. It's in ..., When's your sports day? - It's in ...",
            "stress": "Phonics: February, July",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 10: Our summer holidays": {
            "vocabulary": "beach, campsite, countryside, Bangkok, London, Sydney, Tokyo, last, yesterday, at, on, in (+ place)",
            "structures": "Were you ... last weekend? - Yes, I was. / No, I wasn't., Where were you last summer? - I was in ...",
            "stress": "Phonics: were, where",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 11: My home": {
            "vocabulary": "road, street, big, busy, live, noisy, quiet, at, in (+ name of the street / road)",
            "structures": "Where do you live? - I live ..., What's the ... like? - It's ...",
            "stress": "Phonics: big, street",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 12: Jobs": {
            "vocabulary": "actor, farmer, nurse, office worker, policeman, factory, farm, hospital, nursing home",
            "structures": "What does he / she do? - He's / She's ..., Where does he / she work? - He / She works ...",
            "stress": "Phonics: farmer, nurse",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 13: Appearance": {
            "vocabulary": "big, short, slim, tall, eyes, face, hair, long, round",
            "structures": "What does he / she look like? - He's / She's ..., What does he / she look like? - He / She has ...",
            "stress": "Phonics: long, round",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 14: Daily activities": {
            "vocabulary": "at noon, in the afternoon, in the evening, in the morning, clean the floor, help with the cooking, wash the clothes, wash the dishes",
            "structures": "When do you watch TV? - I watch TV ..., What do you do in the morning? - I ...",
            "stress": "Phonics: watch, wash",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 15: My family's weekends": {
            "vocabulary": "cinema, shopping centre, sports centre, swimming pool, cook meals, do yoga, play tennis, watch films",
            "structures": "Where does he / she go on Saturdays? - He / She goes to the ..., What does he / she do on Sundays? - He / She ...",
            "stress": "Phonics: go, television",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 16: Weather": {
            "vocabulary": "cloudy, rainy, sunny, weather, windy, bakery, bookshop, food stall, water park",
            "structures": "What was the weather like last weekend? - It was ..., Do you want to go to the ...? - Great! Let's go. / Sorry, I can't.",
            "stress": "Stress: 'sunny, 'rainy",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 17: In the city": {
            "vocabulary": "get, go straight, left, right, stop, turn, turn left, turn right, turn round",
            "structures": "What does it say? - It says '...', How can I get to the ...?",
            "stress": "Stress: 'bookshop, 'campsite",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 18: At the shopping centre": {
            "vocabulary": "behind, between, near, opposite, gift shop, skirt, T-shirt, dong, thousand",
            "structures": "Where's the bookshop? - It's ..., How much is the ...? - It's ...",
            "stress": "Stress: be'hind, be'tween",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 19: The animal world": {
            "vocabulary": "crocodiles, giraffes, hippos, lions, dance beautifully, roar loudly, run quickly, sing merrily",
            "structures": "What are these animals? - They're ..., Why do you like ...? - Because they ...",
            "stress": "Stress: 'loudly, 'quickly",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 20: At summer camp": {
            "vocabulary": "building a campfire, dancing around the campfire, playing card games, playing tug of war, putting up a tent, singing songs, taking a photo, telling a story",
            "structures": "What's he / she doing? - He's / She's ..., What are they doing? - They're ...",
            "stress": "Stress: 'visit, 'email",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        }
        # === KẾT THÚC DỮ LIỆU LỚP 4 ===
    },
    "5": {
        # === BẮT ĐẦU DỮ LIỆU LỚP 5 (Đầy đủ) ===
        "Unit 1: All about me!": {
            "vocabulary": "city, class, countryside, dolphin, pink, sandwich, table tennis.",
            "structures": "Can you tell me about yourself?, I'm in ..., I live in the ..., What's your favourite ...?, It's ...",
            "stress": "'dolphin, 'tennis",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 2: Our homes": {
            "vocabulary": "building, flat, house, tower, numbers (23, 38, 93, 116).",
            "structures": "Do you live in this / that ...?, Yes, I do. / No, I don't., What's your address?, It's ...",
            "stress": "fif'teen, six'teen",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 3: My foreign friends": {
            "vocabulary": "American, Australian, Japanese, Malaysian, active, clever, friendly, helpful.",
            "structures": "What nationality is he / she?, He's / She's ..., What's he / she like?, He's / She's ...",
            "stress": "'active, 'friendly",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 4: Our free-time activities": {
            "vocabulary": "go for a walk, play the violin, surf the Internet, water the flowers, always, often, sometimes, usually.",
            "structures": "What do you like doing in your free time?, I like ..., What do you do at the weekend?, I ...",
            "stress": "'always, 'sometimes",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 5: My future job": {
            "vocabulary": "firefighter, gardener, reporter, writer, grow flowers, report the news, teach children, write stories.",
            "structures": "What would you like to be in the future?, I'd like to be a ..., Why would you like to be a ...?, Because I'd like to ...",
            "stress": "'teacher, 'dentist",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 6: Our school rooms": {
            "vocabulary": "first floor, ground floor, second floor, third floor, go along, go downstairs, go past, go upstairs.",
            "structures": "Where's the ...?, It's on the ..., Could you tell me the way to the computer room, please?",
            "stress": "up'stairs, down'stairs",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 7: Our favourite school activities": {
            "vocabulary": "do projects, play games, read books, solve maths problems, difficult, easy, fun, good for group work, useful, interesting.",
            "structures": "What school activity does he / she like?, He / She likes ..., Why does he / she like ...?, Because he / she thinks it's ...",
            "stress": "'solving, 'reading",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 8: In our classroom": {
            "vocabulary": "above, beside, in front of, under, crayon, glue stick, pencil sharpener, set square.",
            "structures": "Where are the ...?, They're ..., Whose ... is this?, It's ...",
            "stress": "a'bove, be'side",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 9: Our outdoor activities": {
            "vocabulary": "aquarium, campsite, funfair, theatre, dance around the campfire, listen to music, play chess, watch the fish.",
            "structures": "Were you at the ... yesterday?, Yes, we were. / No, we weren't., What did you do yesterday?, We ...",
            "stress": "'cinema, 'bakery",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        },
        "Unit 10: Our school trip": {
            "vocabulary": "Ba Na Hills, Bai Dinh Pagoda, Hoan Kiem Lake, Suoi Tien Theme Park, plant trees, play games, visit the old buildings, walk around the lake.",
            "structures": "Did they go to ...?, Yes, they did. / No, they didn't., What did they do there?, They ...",
            "stress": "No'vember, De'cember",
            "types": ['mcq', 'fill', 'scramble', 'match', 'writing', 'reading']
        }
        # === KẾT THÚC DỮ LIỆU LỚP 5 ===
    }
}
# ==========================================================

def extract_json_from_text(text):
    """Trích xuất chuỗi JSON từ văn bản có thể chứa markdown."""
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    # Tìm kiếm JSON mở rộng nhất có thể
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        grade = data.get('grade')         # LẤY KHỐI LỚP
        unit_name = data.get('unit')      # LẤY TÊN UNIT
        types_requests = data.get('types')

        if not all([grade, unit_name, types_requests]):
            return jsonify({'error': 'Thiếu thông tin khối lớp, unit hoặc dạng bài.'}), 400

        # --- Logic lấy dữ liệu chương trình học (ĐÃ CẬP NHẬT) ---
        if grade not in CURRICULUM_DATA:
            return jsonify({'error': f'Không tìm thấy dữ liệu cho khối lớp {grade}.'}), 404
        
        if unit_name not in CURRICULUM_DATA[grade]:
            # Lỗi này xảy ra nếu tên unit trong script.js và app.py không khớp
            return jsonify({'error': f'Không tìm thấy dữ liệu cho Unit: "{unit_name}" của khối lớp {grade}. Vui lòng kiểm tra backend.'}), 404

        # Lấy dữ liệu cụ thể cho unit này
        unit_data = CURRICULUM_DATA[grade][unit_name]
        
        # (Xóa kiểm tra "CHƯA CÓ" vì chúng ta đã điền rồi)

        # --- Xây dựng chuỗi yêu cầu ---
        request_descriptions = []
        for req in types_requests:
            type_name = req.get('type')
            difficulty = req.get('difficulty', 'Trung bình') # Lấy độ khó
            count = int(req.get('count', 0))
            
            # Lọc các dạng bài không được hỗ trợ bởi unit này
            if count > 0 and type_name in unit_data["types"]:
                if type_name == 'reading':
                    request_descriptions.append(f"- {count} bài đọc hiểu (độ khó {difficulty}), mỗi bài có 3-5 câu hỏi.")
                else:
                    request_descriptions.append(f"- {count} câu hỏi thuộc dạng '{type_name}' (độ khó {difficulty})")
        
        if not request_descriptions:
            return jsonify({'error': 'Không có dạng bài hợp lệ nào được chọn hoặc được hỗ trợ cho Unit này.'}), 400

        requests_string = "\n".join(request_descriptions)

        # === PROMPT ĐÃ ĐƯỢC CẬP NHẬT LINH ĐỘNG ===
        prompt = f"""
Act as a strict JSON-generating expert English teacher for {grade}th-grade students in Vietnam.
Your task is to generate a quiz for: **{unit_name}**.

**CRITICAL RULE:** All generated questions MUST STRICTLY and EXCLUSIVELY use the vocabulary, grammatical structures, 
and reflect the phonics/stress patterns specified below for this Unit. For Grade 1, focus on simple vocabulary recognition and sentence patterns.

**DIFFICULTY LEVEL GUIDELINES (Apply gently for Grade 1):**
- **Dễ (Easy):** Direct recall. Use vocabulary and structures in their simplest form (e.g., "What is this? - It is a book.").
- **Trung bình (Medium):** Simple inference or combining concepts (e.g., "I have a [book/car]." or matching "Cc" to "cat").
- **Khó (Hard):** Understanding simple context, unscrambling 3-word sentences. For multiple-choice, distractors should be plausible (e.g., other vocabulary from the same unit).

**CRITICAL RULE 2 (NO AMBIGUITY):** For all multiple-choice questions ('mcq' and within 'reading'), 
there must be only ONE single, unambiguously correct answer. The other three options (distractors) must be clearly and definitively wrong.

**CRITICAL RULE 3 (NO SUBJECTIVITY - ALL TYPES):** Absolutely NO subjective questions asking about personal preferences, likes, 
favorites, or opinions (e.g., "What's your favourite...", "Do you like...", "My favourite is ___.", "I like to ___."). 
This applies strictly to ALL question types, including 'mcq', 'fill', and 'writing'. All questions and required answers MUST be objective 
and verifiable based ONLY on the provided curriculum data or explicit context within the question itself.

**CRITICAL RULE 4 (UNIQUE MATCHING ITEMS):** For 'match' questions, ALL items in the left column ('q' in pairs) MUST be unique, and ALL items in the right column ('a' in pairs) MUST be unique. Do NOT repeat items within the same column.
- **Bad Example (Duplicate 'a'):** pairs: [{{"q": "Hi, I'm", "a": "Bill"}}, {{"q": "Bye,", "a": "Bill"}}]
- **Good Example:** pairs: [{{"q": "Hi, I'm Bill.", "a": "Greeting"}}, {{"q": "Bye, Bill.", "a": "Farewell"}}]

**REVISED CRITICAL RULE 5 (CONTEXTUAL & OBJECTIVE BLANKS - FILL/WRITING):** For BOTH 'fill' questions (with '___') and 'writing' questions involving sentence completion, the sentence MUST provide sufficient specific context clues so that ONLY ONE logical and objective answer from the unit's vocabulary fits the blank. Do NOT create blanks that rely on general knowledge, personal preference, or subjective descriptions (like 'beautiful', 'nice', 'favorite', 'like').
    - Bad (Subjective Fill): 'My favourite food is ___.'
    - Bad (Ambiguous Writing): 'This is a beautiful color. It's ___.'
    - Bad (Subjective Writing): 'I like to play sport. My favourite is ___.'
    - Good (Contextual Fill): 'A ___ flies in the sky.' (Answer: kite)
    - Good (Contextual Writing): 'Look at the apple. It's ___.' (Answer: red)
    - Good (Contextual Writing): 'He works on a farm. He is a ___.' (Answer: farmer)
        
**CURRICULUM DATA FOR THIS SPECIFIC UNIT ({unit_name}):**
---
- **Vocabulary/Phonics:** {unit_data["vocabulary"]}
- **Structures:** {unit_data["structures"]}
- **Stress:** {unit_data["stress"]}
---

**USER REQUEST:**
Based on the curriculum data above, please generate a quiz with the following composition:
{requests_string}

**JSON OUTPUT REQUIREMENTS:**
- Your response MUST ONLY be a single, valid JSON object. No explanations or markdown.
- Every question object MUST have a "type" field.
- **'mcq':** "type", "question", "options" (array of 4 strings), "answer".
- **'fill':** "type", "question" (with '___'), "answer".
- **'scramble':** "type", "question" (jumbled words), "answer".
- **'match':** "type", "question", "pairs" (array of objects with "q" and "a"), "answer". (Ensure 'q' values are unique, and 'a' values are unique).
- **'writing':** "type", "question", "answer". Create meaningful tasks like sentence completion (e.g., "I like ___.") or answering simple questions (e.g., "What is this?"). **Do NOT create simple 'copy this sentence' tasks.**
- **'reading':** (Only if requested and supported)
    - "type": "reading"
    - "passage": "A short paragraph relevant to the unit."
    - "sub_questions": An array of 3-5 question objects (mix 'mcq' and 'true_false').
        - "type": "mcq", "question", "options" (array of 4 strings), "answer".
        - "type": "true_false", "question", "answer" (string: "True" or "False").

The final structure MUST be: {{"questions": [...]}}.
"""
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        request_options = {"timeout": 180}
        response = model.generate_content(prompt, request_options=request_options)
        
        cleaned_text = extract_json_from_text(response.text)

        if not cleaned_text:
            print(f"Gemini response could not be cleaned:\n{response.text}")
            return jsonify({'error': 'AI đã trả về một định dạng không hợp lệ.'}), 500
            
        quiz_data = json.loads(cleaned_text)
        return jsonify(quiz_data)

    except Exception as e:
        print(f"An error occurred in generate_quiz: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-explanation', methods=['POST'])
def get_explanation():
    try:
        data = request.get_json()
        grade = data.get('grade', '5') # Lấy khối lớp, mặc định là 5 nếu không có
        question = data.get('question')
        user_answer = data.get('userAnswer')
        correct_answer = data.get('correctAnswer')

        if not all([question, correct_answer]):
            return jsonify({'error': 'Thiếu câu hỏi hoặc đáp án đúng.'}), 400

        if not user_answer:
            user_answer = "(Học sinh đã không trả lời câu này)"

        # Prompt giải thích được cập nhật linh động theo khối lớp
        prompt = f"""You are a friendly English tutor for a {grade}th-grade student in Vietnam. The student answered incorrectly.
- Question: "{question}"
- Their answer: "{user_answer}"
- Correct answer: "{correct_answer}"
Provide a very simple, short, encouraging explanation in Vietnamese appropriate for a {grade}th-grade student. Start with "Cố lên nhé!".
Return a valid JSON object: {{"explanation": "Your explanation here"}}. Do not include markdown.
"""
        
        model = genai.GenerativeModel('gemini-2.5-flash') # Đã sửa lỗi typo ở đây
        request_options = {"timeout": 120}
        response = model.generate_content(prompt, request_options=request_options)
        
        cleaned_text = extract_json_from_text(response.text)
        if not cleaned_text:
            return jsonify({'explanation': 'Lỗi: AI trả về định dạng không hợp lệ.'})

        explanation_data = json.loads(cleaned_text)
        return jsonify(explanation_data)

    except Exception as e:
        print(f"An error occurred during explanation generation: {e}")
        return jsonify({'error': str(e)}), 500

from waitress import serve
if __name__ == "__main__":
    print("🚀 Server đang khởi chạy tại cổng 5000...")
    print("Hãy mở một terminal khác và chạy 'ngrok http 5000'")
    serve(app, host="0.0.0.0", port=5000)