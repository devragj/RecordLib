import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import SentenceWrapper from "./Sentence";
import ShowHideList from "./ShowHideList";
import EditBox from "./EditBox"
import { editField } from "../actions"

function ChargeWithExpungements(props) {
    const { id, offense, grade, statute, disposition, sentences, modifier, isExpungeable, reason } = props;
    const chargeStyle = { display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px' };
    const reasonColor = isExpungeable? 'green': 'red';
    const reasonStyle = { gridColumn: "1 / 3", color: reasonColor };

    const sentencesRendered = sentences.map(sentenceId => {
            return <SentenceWrapper key={sentenceId} sentenceId={sentenceId}/>
        }
    );

    return (
        <div className="charge" id={id} style={chargeStyle}>
            <div style={reasonStyle}>{reason}</div>
            <div>Offense: {offense}</div>
            <EditBox title="Grade: " item={grade} modifier={modifier} />
            <div>Statute: {statute}</div>
            <div>Disposition: {disposition}</div>
            {sentences.length > 0 &&

                <div style={{gridColumn: "1 / 3"}}>
                        <ShowHideList hidden={true} title="Sentences" list={sentencesRendered} />
                </div>
            }
        </div>
    );
}

ChargeWithExpungements.propTypes = {
    charge_id: PropTypes.string,
    offense: PropTypes.string,
    grade: PropTypes.string,
    statute: PropTypes.string,
    disposition: PropTypes.string,
    sentences: PropTypes.array.isRequired,
    isExpungeable: PropTypes.bool,
    reason: PropTypes.string
}

function mapStateToProps(state, ownProps) {
    return state.entities.charges[ownProps.chargeId];
};

function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: item => {
            dispatch(editField('charges', ownProps.chargeId, 'grade', item))
        }
    };
};

const ChargeWithExpungementsWrapper = connect(mapStateToProps, mapDispatchToProps)(ChargeWithExpungements);
export default ChargeWithExpungementsWrapper;