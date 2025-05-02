from flask import Flask
from flask import render_template, jsonify
from flask import Response, request, redirect, url_for
app = Flask(__name__)
import re

# Data Model
items = [
    {
        "id": 1, 
        "title": "Starry Night", 
        "original_artist": "Vincent van Gogh", 
        "media_url": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Van_Gogh_-_Starry_Night_2.jpg", 
        "description": "A swirling night sky over a tranquil town, known for its vibrant energy and dynamic brushwork.", 
        "price": 250.00,
        "genres": ["Post-Impressionism", "Landscape"]
    },
    {
        "id": 2,
        "title": "The Persistence of Memory",
        "original_artist": "Salvador Dalí",
        "media_url": "https://live.staticflickr.com/3956/15694508911_30fc70b1e1_b.jpg",
        "description": "A surreal composition featuring melting clocks and an otherworldly landscape that challenges the perception of time.",
        "price": 300.00,
        "genres": ["Surrealism", "Abstract"]
    },
    {
        "id": 3,
        "title": "The Scream",
        "original_artist": "Edvard Munch",
        "media_url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Edvard_Munch%2C_The_Scream%2C_1893%2C_National_Gallery%2C_Oslo_%281%29_%2835658212823%29.jpg",
        "description": "A haunting portrayal of existential angst set against a turbulent landscape of bold, emotional colors.",
        "price": 275.00,
        "genres": ["Expressionism", "Landscape"]
    },
    {
        "id": 4,
        "title": "Night in Saint Cloud",
        "original_artist": "Edvard Munch",
        "media_url": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Night_in_Saint-Cloud.jpg",
        "description": "A dramatic portrayal of the descent of night, with bold, expressive strokes capturing the raw emotions of twilight.",
        "price": 320.00,
        "genres": ["Expressionism", "Realism"]
    },
    {
        "id": 5,
        "title": "The Kiss",
        "original_artist": "Gustav Klimt",
        "media_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRw0kgRko3TTjdmyj0hFjks4zZrECz5cfK7zQ&s",
        "description": "A lavish portrayal of intimacy, rendered in vibrant hues with intricate patterns that evoke a sense of tender emotion.",
        "price": 350.00,
        "genres": ["Symbolism", "Abstract"]
    },
    {
        "id": 6,
        "title": "American Gothic",
        "original_artist": "Grant Wood",
        "media_url": "https://live.staticflickr.com/6025/5964306788_3642aaaf9a_b.jpg",
        "description": "A stark portrayal of rural American life, capturing the somber spirit of a farmhouse and its stoic inhabitants.",
        "price": 200.00,
        "genres": ["Realism", "Landscape"]
    },
    {
        "id": 7,
        "title": "Water Lilies",
        "original_artist": "Claude Monet",
        "media_url": "https://storage.googleapis.com/pod_public/1300/227292.jpg",
        "description": "A serene, impressionistic depiction of nature's reflective beauty, rendered in soft, luminous brush strokes.",
        "price": 280.00,
        "genres": ["Impressionism", "Landscape"]
    },
    {
        "id": 8,
        "title": "Campbell's Soup Cans",
        "original_artist": "Andy Warhol",
        "media_url": "https://live.staticflickr.com/65535/51190651527_89903014cc_b.jpg",
        "description": "A bold, repetitive display of everyday consumer culture transformed into iconic pop art imagery.",
        "price": 150.00,
        "genres": ["Pop Art", "Abstract"]
    },
    {
        "id": 9,
        "title": "The Son of Man",
        "original_artist": "René Magritte",
        "media_url": "https://live.staticflickr.com/2411/2065975725_16a8dd1958.jpg",
        "description": "An enigmatic portrait featuring a man with his face mysteriously obscured, inviting viewers to explore hidden depths of meaning.",
        "price": 265.00,
        "genres": ["Surrealism", "Abstract"]
    },
    {
        "id": 10,
        "title": "Composition VII",
        "original_artist": "Wassily Kandinsky",
        "media_url": "https://cdn2.picryl.com/photo/1913/12/31/vassily-kandinsky-1913-composition-7-e460dc-640.jpg",
        "description": "A vibrant explosion of color and form that captures the essence of abstract expression through dynamic composition.",
        "price": 310.00,
        "genres": ["Abstract", "Expressionism"]
    }
]

# Jinja2 to highlight matched query substring
@app.template_filter('highlight')
def highlight(text, query):
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f'<span class="highlight">{m.group(0)}</span>', text)

@app.route('/')
def home():
    return render_template('homepage.html', items=items)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    results = [item for item in items if query.lower() in item['title'].lower() or 
                                      query.lower() in item['description'].lower() or 
                                      query.lower() in item['original_artist'].lower()]
    return render_template('search_results.html', query=query, results=results, count=len(results))

@app.route('/view/<int:item_id>')
def view_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    next_item = next((i for i in items if i["id"] != item_id), None)
    return render_template('item_details.html', item=item, next_item=next_item)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    possible_genres = ["Post-Impressionism", "Landscape", "Surrealism", "Abstract", "Expressionism", "Realism", "Symbolism", "Impressionism", "Pop Art"]
    item = next((item for item in items if item["id"] == item_id), None)
    if request.method == 'POST':
        if request.form.get('action') == 'discard':
            return redirect(url_for('view_item', item_id=item_id))
        title = request.form.get('title', '').strip()
        original_artist = request.form.get('original_artist', '').strip()
        media_url = request.form.get('media_url', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        genres = request.form.getlist('genres')

        errors = {}
        if not title:
            errors['title'] = "Error: Title is empty"
        if not original_artist:
            errors['original_artist'] = "Error: Original Artist is empty"
        if not media_url:
            errors['media_url'] = "Error: Media URL is empty"
        if not description:
            errors['description'] = "Error: Description is empty"
        try:
            price_val = float(price)
            if price_val <= 0:
                errors['price'] = "Error: Price should be a positive number."
        except ValueError:
            errors['price'] = "Error: Price should be a positive number."
        if not genres:
            errors['genres'] = "Error: At least one genre must be selected."

        if errors:
            return render_template('edit_item.html', item=item, errors=errors, possible_genres=possible_genres)

        item['title'] = title
        item['original_artist'] = original_artist
        item['media_url'] = media_url
        item['description'] = description
        item['price'] = price_val
        item['genres'] = genres
        return redirect(url_for('view_item', item_id=item_id))

    return render_template('edit_item.html', item=item, errors={}, possible_genres=possible_genres)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    possible_genres = ["Post-Impressionism", "Landscape", "Surrealism", "Abstract", "Expressionism", "Realism", "Symbolism", "Impressionism", "Pop Art"]
    if request.method == 'POST':
        form_data = { key: request.form.getlist(key) if key == 'genres' else request.form.get(key, '').strip() 
                      for key in request.form }
        title = form_data.get('title', '')
        original_artist = form_data.get('original_artist', '')
        media_url = form_data.get('media_url', '')
        description = form_data.get('description', '')
        price = form_data.get('price', '')
        genres = form_data.get('genres', [])

        errors = {}
        if not title:
            errors['title'] = "Error: Title is empty"
        if not original_artist:
            errors['original_artist'] = "Error: Original Artist is empty"
        if not media_url:
            errors['media_url'] = "Error: Media URL is empty"
        if not description:
            errors['description'] = "Error: Description is empty"
        try:
            price_val = float(price)
            if price_val <= 0:
                errors['price'] = "Error: Price should be a positive number."
        except:
            errors['price'] = "Error: Price should be a positive number."
        if not genres:
            errors['genres'] = "Error: At least one genre must be selected."
        
        if errors:
            return render_template('add_item.html', success=False, errors=errors, possible_genres=possible_genres, form_data=form_data)
            # return jsonify(success=False, errors=errors)
        
        new_id = max(item["id"] for item in items) + 1
        new_item = {
            "id": new_id,
            "title": title,
            "original_artist": original_artist,
            "media_url": media_url,
            "description": description,
            "price": price_val,
            "genres": genres
        }
        items.append(new_item)
        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return jsonify(success=True, new_item_id=new_item["id"])
        return render_template('add_item.html', success=True, errors={}, new_item=new_item, possible_genres=possible_genres, form_data={})

    return render_template('add_item.html', errors={}, possible_genres=possible_genres, form_data={})


if __name__ == '__main__':
   app.run(debug = True, port=5001)