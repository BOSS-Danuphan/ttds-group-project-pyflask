import React, {Component} from 'react';
import {TwitterTweetEmbed} from 'react-twitter-embed';
import './ResultsWall.css';

class ResultsWall extends Component {

    // <TwitterTweetEmbed tweetId='653229520015749121' options={{'height': '400', 'width':400}}/>
    render() {
        const tweetOption = {'conversation': 'none'}
        const tweetList = this.props.stTweets.map((tweet, index) =>
            <li key={tweet}><TwitterTweetEmbed tweetId={tweet} options={tweetOption}/></li>
        );
        const rtTweetList= this.props.rtTweets.map((tweet, index) =>
            <li key={tweet}><TwitterTweetEmbed tweetId={tweet} options={tweetOption}/></li>
        );
        return (
            <div className="ResultsWall">
                <div className="ResultsWall-static">
                    <h3>Ranked Results: </h3>
                    <ul>{tweetList.length ? tweetList : 'No results'}</ul>
                </div>
                <div className="ResultsWall-realtime">
                    <h3>Real-time results:</h3>
                    <ul>{rtTweetList.length ? rtTweetList : 'No results'}</ul>
                </div>
            </div>
        );
    }
}

export default ResultsWall;
