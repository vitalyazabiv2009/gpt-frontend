from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

API_BASE = 'https://api.gpt.mws.ru/v1'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = request.form['api_key']
        session['api_key'] = api_key
        return redirect(url_for('select_model'))
    return render_template('index.html')

@app.route('/models')
def select_model():
    api_key = session.get('api_key')
    if not api_key:
        return redirect(url_for('index'))
    
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(f'{API_BASE}/models', headers=headers)
    
    if response.status_code != 200:
        return f"Ошибка: {response.status_code} - {response.text}"
    
    models = response.json()['data']
    return render_template('models.html', models=models)

@app.route('/chat/<model_id>', methods=['GET', 'POST'])
def chat(model_id):
    api_key = session.get('api_key')
    if not api_key:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_message = request.form['message']
        history = session.get('chat_history', [])
        history.append({"role": "user", "content": user_message})
        
        try:
            response = requests.post(
                f'{API_BASE}/chat/completions',
                headers={'Authorization': f'Bearer {api_key}'},
                json={
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": "Ты помощник"},
                        *history
                    ],
                    "temperature": 0.6
                }
            )
            
            if response.status_code != 200:
                return f"Ошибка API: {response.status_code} - {response.text}"
            
            # Извлекаем ответ с проверкой структуры
            response_data = response.json()
            assistant_reply = response_data['choices'][0]['message']['content']
            role = response_data['choices'][0]['message']['role']
            
            # Сохраняем только user/assistant сообщения
            history.append({"role": role, "content": assistant_reply})
            session['chat_history'] = history[-20:]  # Ограничиваем историю
            
            return render_template('chat.html', model_id=model_id, history=history)
            
        except Exception as e:
            return f"Ошибка обработки: {str(e)}"
    
    session['chat_history'] = []
    return render_template('chat.html', model_id=model_id, history=[])

@app.errorhandler(Exception)
def handle_exception(e):
    return f"Произошла ошибка: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)