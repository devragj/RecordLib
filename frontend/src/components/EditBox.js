import React, { useState } from "react";
import PropTypes from 'prop-types';

/**
 * This component wraps a single field and allows
 * it to be edited.
 * The user can click on the editable value,
 * or on its label.
 * This will reveal a textbox, within which the
 * value can be edited.
 * The new value is sent to the redux store.
 * Pressing Enter in the textbox will hide it again.
 * @param {Object} props
 * @constructor
 */
function EditBox(props) {
        const { title, item, modifier } = props;
        const [edit, setEdit] = useState(false);
        const label = title;

        const handleItemClick = () => setEdit(true);
        const handleLabelClick = () => {
                if (!edit) {
                        setEdit(true);
                }
        }

        const handleChange = event => modifier(event.target.value);
        const handleKey = event => {
                if (event.key === 'Enter') {
                        setEdit(false);
                }
        }

        return (
                <div className="editBox">
                    <span onClick={handleLabelClick}>{label}</span> {!edit
                            ? <span onClick={handleItemClick}>{item}</span>
                            :  <input type="text" value={item} onChange={handleChange} onKeyUp={handleKey}/>
                        }
                </div>
        );
}

EditBox.propTypes = {
    /**
     * The label of the component, describing the contents.
     */
    title: PropTypes.string.isRequired,
    /**
     * The value which can be edited.
     */
    item: PropTypes.string.isRequired,
    /**
     * The callback which registers the change.
     */
    modifier: PropTypes.func.isRequired
}

export default EditBox;