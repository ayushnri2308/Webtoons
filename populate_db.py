from app import db,app
from models import Webtoon

# Predefined webtoon data
webtoons = [
    {
        'title': 'Castle Swimmer',
        'summary': 'A mermaid prophecy and a beacon of hope.',
        'characters': ['Kappa', 'Siren', 'Turtle Prince']
    },
    {
        'title': 'Tower of God',
        'summary': 'A boy enters a mysterious tower to reunite with his best friend.',
        'characters': ['Bam', 'Rachel', 'Khun Aguero Agnis']
    },
    # Add more webtoons here
]

def populate_db():
    for webtoon_data in webtoons:
        if not Webtoon.query.filter_by(title=webtoon_data['title']).first():
            new_webtoon = Webtoon(
                title=webtoon_data['title'],
                summary=webtoon_data['summary'],
                characters=webtoon_data['characters']
            )
            db.session.add(new_webtoon)
    
    db.session.commit()
    print('Database populated successfully!')

if __name__ == '__main__':
    # Add data to the database
    with app.app_context():
        populate_db()
