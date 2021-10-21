import React, { useEffect, useState } from 'react';
import ChatBot from 'react-simple-chatbot';
import QUESTIONS from './questions.json';
import './App.css';

function MovieCard({ name, imageID }) {
  return (
    <p style={{ textAlign: 'center' }}>
      {console.log(name, imageID)}
      <img
        src={`https://img.omdbapi.com/?apikey=46f4f775&i=${imageID}`}
        alt='Poster'
      />
      <br />
      <h3 style={{ width: '214px' }}>{name}</h3>
    </p>
  );
}

function Review({ steps, triggerNextStep }) {
  const { actor, genre, keywords, director } = steps;

  const [loading, setLoading] = useState(true);
  const [moviesList, setMoviesList] = useState(['No movies Found:(']);
  useEffect(() => {
    loading &&
      fetch(
        'http://localhost:5000/get?' +
          new URLSearchParams({
            actor: actor.value,
            genre: genre.value,
            keywords: keywords.value,
            director: director.value,
          })
      )
        .then((response) => response.json())
        .then((data) => {
          setMoviesList(data.movies);
          setLoading(false);
          triggerNextStep({ trigger: 'end-message' });
        })
        .catch((err) => console.log(err));
  }, [actor, genre, keywords, director, loading, triggerNextStep]);

  return (
    <div>
      {loading && 'Loading...'}
      {!loading &&
        moviesList.map((e, i) => (
          <MovieCard key={i} name={e.name} imageID={e.id} />
        ))}
    </div>
  );
}

export default function App() {
  return (
    <div className='app'>
      <ChatBot
        className='chatEele'
        headerTitle='Movie Recommendation'
        customDelay={50}
        userDelay={100}
        width='900px'
        steps={[
          {
            id: '1',
            message: QUESTIONS.GENRE,
            trigger: 'genre',
          },
          {
            id: 'genre',
            user: true,
            validator: (e) => {
              if (e === '') return 'Cannot parse empty string';
              else return true;
            },
            trigger: '2',
          },
          {
            id: '2',
            message: QUESTIONS.ACTOR,
            trigger: 'actor',
          },
          {
            id: 'actor',
            user: true,
            validator: (e) => {
              if (e === '') return 'Cannot parse empty string';
              else return true;
            },
            trigger: '3',
          },
          {
            id: '3',
            message: QUESTIONS.DIRECTOR,

            trigger: 'director',
          },
          {
            id: 'director',
            user: true,
            validator: (e) => {
              if (e === '') return 'Cannot parse empty string';
              else return true;
            },
            trigger: '4',
          },
          {
            id: '4',
            message: QUESTIONS.KEYWORDS,
            trigger: 'keywords',
          },
          {
            id: 'keywords',
            user: true,
            validator: (e) => {
              if (e === '') return 'Cannot parse empty string';
              else return true;
            },
            trigger: 'results',
          },
          {
            id: 'results',
            component: <Review />,
            waitAction: true,
            asMessage: true,
            // trigger: 'end-message',
          },
          {
            id: 'end-message',
            options: [
              {
                value: 'restart',
                label: 'Play Again?',
                trigger: '1',
              },
            ],
          },
        ]}
      />
    </div>
  );
}
