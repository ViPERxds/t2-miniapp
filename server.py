from flask import Flask, send_from_directory, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Создаем базу данных и таблицу
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT NOT NULL,
                  date TEXT NOT NULL,
                  time TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  UNIQUE(date, time))''')
    conn.commit()
    conn.close()

# Инициализируем базу при запуске
init_db()

# Путь к директории с HTML файлами
STATIC_DIR = 'static'  # Упрощаем путь к статическим файлам

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(STATIC_DIR, path)

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'first.html')

# Обработка бронирований
@app.route('/update_bookings', methods=['POST'])
def update_bookings():
    try:
        data = request.json
        time = data['time']
        date = data['date']
        
        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        
        c.execute('''INSERT INTO bookings (time, date, count) 
                    VALUES (?, ?, 1) 
                    ON CONFLICT(time, date) 
                    DO UPDATE SET count = count + 1''', (time, date))
        
        c.execute('SELECT count FROM bookings WHERE time = ? AND date = ?', (time, date))
        result = c.fetchone()
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': result[0]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/get_bookings', methods=['POST'])
def get_bookings():
    try:
        data = request.json
        time = data['time']
        date = data['date']
        
        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        
        # Считаем количество бронирований для этого времени и даты
        c.execute('SELECT COUNT(*) FROM bookings WHERE time = ? AND date = ?', (time, date))
        count = c.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Добавляем новые маршруты для работы с бронированиями
@app.route('/api/book-slot', methods=['POST'])
def book_slot():
    data = request.json
    user_id = data.get('userId')
    date = data.get('date')
    time = data.get('time')
    
    if not all([user_id, date, time]):
        return jsonify({'success': False, 'error': 'Missing required fields'})
    
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    
    # Проверяем, не забронировано ли уже это время
    cursor.execute('''
        SELECT id FROM bookings 
        WHERE date = ? AND time = ?
    ''', (date, time))
    
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Slot already booked'})
    
    # Сохраняем бронь
    cursor.execute('''
        INSERT INTO bookings (user_id, date, time)
        VALUES (?, ?, ?)
    ''', (user_id, date, time))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/booked-slots', methods=['POST'])
def get_booked_slots():
    data = request.json
    date = data.get('date')
    
    if not date:
        return jsonify({'success': False, 'error': 'Date is required'})
    
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    
    # Получаем все забронированные слоты для выбранной даты
    cursor.execute('''
        SELECT time FROM bookings 
        WHERE date = ?
    ''', (date,))
    
    booked_slots = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'bookedSlots': booked_slots
    })

@app.route('/api/booked-dates', methods=['GET'])
def get_booked_dates():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    
    # Получаем уникальные даты, где есть бронирования
    cursor.execute('SELECT DISTINCT date FROM bookings')
    booked_dates = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'bookedDates': booked_dates
    })

if __name__ == '__main__':
    # Создаем необходимые директории, если их нет
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/fonts', exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=True) 