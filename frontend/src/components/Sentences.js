import React from "react";
import PropTypes from 'prop-types';

import SentenceWrapper from "./Sentence";
import AddSentenceWrapper from "./AddSentence";
import ShowHideList from "./ShowHideList";


function Sentences(props) {
    const sentencesStyle = {gridColumn: "1 / 3"};
    const { sentences, chargeId, editing } = props;
    const sentencesRendered = sentences.map(sentenceId => {
            return <SentenceWrapper key={sentenceId} sentenceId={sentenceId}/>
        }
    );

    return (
        <div className="sentences" style={sentencesStyle}>
        {editing &&
            <AddSentenceWrapper chargeId={chargeId} nextIndex={sentences.length} />
        }
        {sentences.length > 0 &&
           <ShowHideList hidden={true} title="Sentences" list={sentencesRendered} />
        }
        </div>
    );
}

Sentences.propTypes = {
    /**
        The list of sentence ids.
    */
    sentences: PropTypes.array.isRequired,
    /**
        The id of the charge containing the sentences.
    */
    chargeId: PropTypes.string.isRequired,
    /**
        This component wil be used either in the Case component,
        in which case editing is false, or in the EditCase
        component, in which case editing is true.
    */
    editing: PropTypes.bool
}

export default Sentences;