import React from "react";
import PropTypes from 'prop-types';

import EditField from "./EditField";
import Sentences from "./Sentences";

/**
 * Component to edit a charge, including supplying values to a newly-created charge.
 */
function EditCharge(props) {
    const { id, offense, grade, statute, disposition, disposition_date, sentences, modifier } = props;
    const chargeStyle = { display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px' };

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */
    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editCharge" id={id} style={chargeStyle}>
            <EditField item={offense} label="Offense: " modifier={getPropertyModifier('offense')} />
            <EditField item={grade} label="Grade: " modifier={getPropertyModifier('grade')} />
            <EditField item={statute} label="Statute: " modifier={getPropertyModifier('statute')} />
            <EditField item={disposition} label="Disposition: " modifier={getPropertyModifier('disposition')} />
            <EditField item={disposition_date} label="Disposition Date: " modifier={getPropertyModifier('disposition_date')} />
            <Sentences sentences={sentences} chargeId={id} editing={true}/>
        </div>
    );
}

EditCharge.propTypes = {
    id: PropTypes.string,
    offense: PropTypes.string,
    grade: PropTypes.string,
    statute: PropTypes.string,
    disposition: PropTypes.string,
    disposition_date: PropTypes.string,
    sentences: PropTypes.array.isRequired,
    modifier: PropTypes.func
}

export default EditCharge;