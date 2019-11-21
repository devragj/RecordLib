import React from "react";
import PropTypes from 'prop-types';

/**
 * This component wraps a single field and allows
 * it to be edited.
 * The new value is sent to the redux store.
 * @constructor
 */
function EditField(props) {
        const { item, label, modifier, fieldType } = props;

        const handleChange = event => modifier(event.target.value);

        return (
                <div className="editField">
                     {label}  <input type={fieldType || "text"} value={item} onChange={handleChange}/>
                </div>
        );
}

EditField.propTypes = {
    /**
     * The label of the component, describing the contents.
     */
    label: PropTypes.string.isRequired,
    /**
     * The value which can be edited.
     */
    item: PropTypes.string.isRequired,
    /**
     * The callback which registers the change.
     */
    modifier: PropTypes.func.isRequired
}

export default EditField;