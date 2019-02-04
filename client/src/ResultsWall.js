import React, {Component} from 'react';
import {TwitterTweetEmbed} from 'react-twitter-embed';
import Fade from 'react-reveal/Fade';
import './ResultsWall.css';

class ResultsWall extends Component {

    // <TwitterTweetEmbed tweetId='653229520015749121' options={{'height': '400', 'width':400}}/>
    // const testTweets = ['653229520015749121', '1092234034284056576', '1092219188989562880', '1092218687392759809', '1092207358426664961']
    render() {
        const tweetOption = {'conversation': 'none'};
        const tweetList = this.props.stTweets
            .slice(0, this.props.numberOfResults)
            .map(tweet => <li key={tweet}><TwitterTweetEmbed tweetId={tweet} options={tweetOption}/></li>);
        const rtTweetList = this.props.rtTweets
            .slice(0, this.props.numberOfResults)
            .map(tweet => <li key={tweet}><TwitterTweetEmbed tweetId={tweet} options={tweetOption}/></li>);

        return (
            <div className="ResultsWall">
                <div className="ResultsWall-static">
                    <h3>Ranked Results: </h3>
                    <Fade cascade>
                        <ul>
                            {tweetList.length ? tweetList : 'No results'}
                        </ul>
                    </Fade>

                </div>
                <div className="ResultsWall-realtime">
                    <h3>Real-time results:</h3>
                    <Fade cascade>
                        <ul>
                            {rtTweetList.length ? rtTweetList : 'No results'}
                        </ul>
                    </Fade>
                </div>
            </div>
        );
    }
}

export default ResultsWall;
