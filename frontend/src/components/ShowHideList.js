import React, { useState } from "react";
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlusCircle, faMinusCircle } from '@fortawesome/free-solid-svg-icons'

/**
 * This component allows a potentially long list of rendered components to be hidden.
 * When the list is hidden, the header of the component has a plus sign icon on its left.
 * Clicking on the icon shows the list and changes the icon to minus.
 */
function ShowHideList(props) {
    const { hidden, list} = props
    const [listHidden, setListHidden] = useState(hidden);

    const handlePlusClick = () => {
            setListHidden(false);
    }

    const handleMinusClick = () => {
            setListHidden(true);
    }

    const iconStyle = {marginLeft: '10px'};

    return (
        <div className="showHideList">
            <h5>{props.title}
                {listHidden?   <FontAwesomeIcon icon={faPlusCircle} style={iconStyle} onClick={handlePlusClick}/>
                    : <FontAwesomeIcon icon={faMinusCircle} style={iconStyle} onClick={handleMinusClick}/>
                }
            </h5>
            {!listHidden && list}
        </div>
    );
}

ShowHideList.propTypes = {
    /**
     * The header of the component, naming or describing the contents.
     */
    title: PropTypes.string.isRequired,
    /**
     * An array of JSX rendered by the containing component.
     */
    list: PropTypes.array.isRequired

}

export default ShowHideList;