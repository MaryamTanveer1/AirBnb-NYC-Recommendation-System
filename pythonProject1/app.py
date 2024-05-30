from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
df = pd.read_csv('C:\\Users\\Saeed\\Desktop\\modified_dataset9.csv')
df['combined_features'] = df['room_type'] + ' ' + df['neighbourhood_group'] + ' ' + df['price'].astype(str) + ' ' + df[
    'minimum_nights'].astype(str)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

batch_size = 1000
def compute_cosine_similarity(tfidf_matrix, batch_size):
    num_rows = tfidf_matrix.shape[0]
    for start in range(0, num_rows, batch_size):
        end = min(start + batch_size, num_rows)
        yield cosine_similarity(tfidf_matrix[start:end], tfidf_matrix)


indices = pd.Series(df.index, index=df['id']).drop_duplicates()
cosine_sim_generator = compute_cosine_similarity(tfidf_matrix, batch_size)


def filter_dataframe(df, selected_room_type, selected_neighbourhood_group, selected_price, selected_minimum_nights,
                     search_name):
    if selected_room_type != 'All Room Types':
        df = df[df['room_type'] == selected_room_type]
    if selected_neighbourhood_group != 'All Neighbourhoods':
        df = df[df['neighbourhood_group'] == selected_neighbourhood_group]
    if selected_price and selected_price != 'All prices':
        df = df[df['price'].astype(int) <= int(selected_price)]
    if selected_minimum_nights and selected_minimum_nights != 'All minimum nights':
        df = df[df['minimum_nights'].astype(int) == int(selected_minimum_nights)]
    if search_name:
        df = df[df.apply(
            lambda x: str(search_name).lower() in str(x['name']).lower() or str(search_name).lower() in str(
                x['neighbourhood']).lower(), axis=1)]
    return df


def get_recommendations(selected_room_type, selected_neighbourhood_group, selected_price, selected_minimum_nights,
                        search_name, df, cosine_sim):
    df_filtered = filter_dataframe(df, selected_room_type, selected_neighbourhood_group, selected_price,
                                   selected_minimum_nights, search_name)

    recommendations = []
    for _, rec in df_filtered.iterrows():
        recommendations.append({
            'name': rec['name'],
            'neighbourhood_group': rec['neighbourhood_group'],
            'neighbourhood': rec['neighbourhood'],
            'price': rec['price'],
            'imagefor_name': rec['imagefor_name'],
            'room_type': rec['room_type'],
            'availability_365': rec['availability_365'],
            'minimum_nights': rec['minimum_nights'],
            'number_of_reviews': rec['number_of_reviews']
        })

    return recommendations


def get_trending_listings(df, selected_room_type, selected_neighbourhood_group, selected_price, selected_minimum_nights,
                          search_name):
    df_filtered = filter_dataframe(df, selected_room_type, selected_neighbourhood_group, selected_price,
                                   selected_minimum_nights, search_name)
    trending_recommendations = df_filtered.sort_values(by='number_of_reviews', ascending=False)
    trending_recommendations = trending_recommendations[:20]  # Display top 20 trending listings

    recommendations = []
    for _, rec in trending_recommendations.iterrows():
        recommendations.append({
            'name': rec['name'],
            'neighbourhood_group': rec['neighbourhood_group'],
            'neighbourhood': rec['neighbourhood'],
            'price': rec['price'],
            'imagefor_name': rec['imagefor_name'],
            'room_type': rec['room_type'],
            'availability_365': rec['availability_365'],
            'minimum_nights': rec['minimum_nights'],
            'number_of_reviews': rec['number_of_reviews']
        })

    return recommendations


def get_top_neighborhoods(df):
    top_neighborhoods = df.groupby('neighbourhood_group')['image_url'].first().reset_index()
    return top_neighborhoods.values.tolist()


room_types = ['All Room Types'] + df['room_type'].unique().tolist()
neighbourhood_groups = ['All Neighbourhoods'] + df['neighbourhood_group'].unique().tolist()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_room_type = request.form.get('room_type', 'All Room Types')
        selected_neighbourhood_group = request.form.get('neighbourhood_group', 'All Neighbourhoods')
        selected_price = request.form.get('price', 'All prices')
        selected_minimum_nights = request.form.get('minimum_nights', 'All minimum nights')
        search_name = request.form.get('search_input', '')

        recommendations = get_recommendations(selected_room_type, selected_neighbourhood_group, selected_price,
                                              selected_minimum_nights, search_name, df, next(cosine_sim_generator))
        trending_recommendations = get_trending_listings(df, selected_room_type, selected_neighbourhood_group,
                                                         selected_price, selected_minimum_nights, search_name)

        return render_template('index.html', room_types=room_types, neighbourhood_groups=neighbourhood_groups,
                               selected_room_type=selected_room_type,
                               selected_neighbourhood_group=selected_neighbourhood_group,
                               selected_price=selected_price, selected_minimum_nights=selected_minimum_nights,
                               recommendations=recommendations, trending_recommendations=trending_recommendations)
    else:
        trending_recommendations = get_trending_listings(df, 'All Room Types', 'All Neighbourhoods', 'All prices',
                                                         'All minimum nights', '')
        top_neighborhoods = get_top_neighborhoods(df)
        return render_template('index.html', room_types=room_types, neighbourhood_groups=neighbourhood_groups,
                               top_neighborhoods=top_neighborhoods, recommendations=[],
                               trending_recommendations=trending_recommendations)
def top_neighbourhoods():
    top_neighborhoods = get_top_neighborhoods(df)
    return render_template('index.html', top_neighborhoods=top_neighborhoods)

if __name__ == '__main__':
    app.run(debug=True)
