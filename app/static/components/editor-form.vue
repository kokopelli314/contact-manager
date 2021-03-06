/**
 * Modal form to add, edit, or view a contact in detail.
 */
<template>
<div class="editor-wrapper">
    <div class="modal">
        <!-- Control buttons in the header -->
        <div class="header">
            <h2>
                <span v-if="addingNewContact">Add Contact</span>
                <span v-else-if="editMode">Edit Contact</span>
                <span v-else>{{ contact.first_name }} {{ contact.last_name }}</span>
            </h2>
            <div class="window-buttons">
                <button v-if="!editMode" @click="editMode=true">
                    <i class="fas fa-pen" title="Edit contact"></i>
                </button>
                <button title="Exit" @click="cancel"><i class="fas fa-times"></i></button>
            </div>
        </div>

        <p class="message" v-if="message">
            {{ message }}
        </p>


        <!-- Name and date of birth fields -->
        <div>
            <label>Name</label>
            <input v-model="contact.first_name" v-if="contact.first_name || editMode"
                placeholder="First name"
                :readonly="!editMode"
                :class="{ readonly: !editMode }"
            />
            <input v-model="contact.last_name" v-if="contact.last_name || editMode"
                placeholder="Last name"
                :readonly="!editMode"
                :class="{ readonly: !editMode }"
            />
        </div>

        <div v-if="contact.date_of_birth || editMode">
            <label>Birthday</label>
            <input v-model="contact.date_of_birth"
                type="date"
                :readonly="!editMode"
                :class="{ readonly: !editMode }"
            />
        </div>


        <!-- The array-based fields take a little more boilerplate. -->
        <!-- If more fields like this are added, consider creating a new
                component type to wrap them. -->
        <div class="field-wrapper" v-if="phone_numbers.length || editMode">
            <label>Phone Numbers</label>
            <button class="add-line green" v-if="editMode"
                title="Add Phone Number"
                @click="addBlankTo('phone_numbers')">
                +
            </button>
            <div class="lines-wrapper" v-for="(num, i) in phone_numbers">
                <input
                    v-model="num.value"
                    :placeholder="'Phone Number ' + (i+1)"
                    :readonly="!editMode"
                    :class="{ readonly: !editMode }"
                />
                <button class="delete-line" @click="phone_numbers.splice(i, 1)"
                    v-if="editMode" title="Remove">X</button>
            </div>
        </div>

        <div class="field-wrapper" v-if="emails.length || editMode">
            <label>Emails</label>
            <button class="add-line green" v-if="editMode"
                title="Add Email"
                @click="addBlankTo('emails')">
                +
            </button>
            <div class="lines-wrapper" v-for="(email, i) in emails">
                <input
                    v-model="email.value"
                    :placeholder="'Email ' + (i+1)"
                    :readonly="!editMode"
                    :class="{ readonly: !editMode }"
                />
                <button class="delete-line" @click="emails.splice(i, 1)"
                    v-if="editMode" title="Remove">X</button>
            </div>
        </div>

        <div class="field-wrapper" v-if="addresses.length || editMode">
            <label>Addresses</label>
            <button class="add-line green" v-if="editMode"
                title="Add Address"
                @click="addBlankTo('addresses')">
                +
            </button>
            <div class="lines-wrapper" v-for="(address, i) in addresses">
                <input
                    v-model="address.value"
                    :placeholder="'Address ' + (i+1)"
                    :readonly="!editMode"
                    :class="{ readonly: !editMode }"
                />
                <button class="delete-line" @click="addresses.splice(i, 1)"
                    v-if="editMode" title="Remove">X</button>
            </div>
        </div>

        <div class="button-wrapper" v-if="editMode">
            <button @click="save" class="save">Save</button>
            <button @click="cancel" class="cancel">Cancel</button>
        </div>
    </div>
</div>
</template>


<script>
'use strict';

const clone = require('ramda/src/clone');

export default {
    props: {
        contact: {
            type: Object,
            default: () => { return {} }
        },
        startInEditMode: {
            type: Boolean,
            default: true
        }
    },

    data () {
        return {
            phone_numbers: [],
            emails: [],
            addresses: [],
            editMode: true,
            message: null
        };
    },

    mounted: function() {
        // set up arrays properly to allow v-model'ing
        this.phone_numbers = loadArray(this.contact.phone_numbers);
        this.emails = loadArray(this.contact.emails);
        this.addresses = loadArray(this.contact.addresses);
        // initialize editing status based on parent
        this.editMode = this.startInEditMode;
    },

    computed: {
        addingNewContact: function() {
            return this.editMode && !this.contact.id;
        }
    },

    methods: {
        save: function() {
            // validate that first name has been filled
            if (!this.contact.first_name) {
                this.message = `First Name required.`;
                window.scrollTo(0, 0);
                return;
            }
            // capitalize names
            function capitalize(s) {
                if (!s) return null;
                return s[0].toUpperCase() + s.substr(1);
            }
            this.contact.first_name = capitalize(this.contact.first_name);
            this.contact.last_name = capitalize(this.contact.last_name);
            // format arrays properly
            this.contact.phone_numbers = saveArray(this.phone_numbers);
            this.contact.emails = saveArray(this.emails);
            this.contact.addresses = saveArray(this.addresses);
            this.$emit('save', clone(this.contact));
            this.message = null;
        },
        cancel: function() {
            this.$emit('cancel');
        },
        /**
         * Add empty `value` object to one of the arrays. Scrolls window down
         * to bring into view, if needed.
         * @param  {String} arrayName addresses, emails, or phone_numbers
         */
        addBlankTo: function(arrayName) {
            this[arrayName].push({ value: '' });
            // make sure bottom of modal is still visible so user can save
            let elRect = this.$el.getBoundingClientRect();
            if (elRect.bottom > window.innerHeight) {
                window.scrollBy(0, 50);
            }
        }
    }
}

// Takes raw array of values and returns array of objects with `value` field
function loadArray(array) {
    if (!array) return [];
    return array.map((a) => ({ value: a }));
}
// Takes array of objects with `value` field and returns array of raw values
function saveArray(array) {
    if (!array) return [];
    // return `truth-y` values
    return array.map((a) => a.value).filter((a) => !!a);
}

function randomColor() {
    let colors = [
        'cadetblue', 'chocolate', 'darkblue', 'darkgreen', 'darkorchid',
        'darksalmon', 'darkviolet', 'gray', 'orangered', 'seagreen', 'tomato'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}
</script>


<style scoped>
.editor-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    min-height: 100vh;
    z-index: 10;
    background-color: hsla(0, 0%, 39%, 0.88);
}
.modal > div.header {
    margin: 0.5em 0 0 0;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.window-buttons {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    min-width: 4em;
}
.window-buttons button {
    background-color: transparent;
    color: inherit;
}
.window-buttons button:hover {
    color: hsl(89, 95%, 54%);
}
.message {
    color: hsl(89, 95%, 54%);
}
.modal {
    display: flex;
    flex-direction: column;
    background-color: #282828;
    margin: 2em auto;
    max-width: 20em;
    padding: 1em;
    border-radius: 4px;
}
.modal > * {
    margin: 1em auto;
    width: 100%;
    line-height: 1.5em;
}
.modal > div {
    margin-top: 0;
}
.modal .field-wrapper {
    position: relative;
}
.modal h2 {
    margin: 0 0 0.5em 0;
}
.modal label {
    display: block;
    font-size: 0.85em;
    margin: 0;
    color: hsl(89, 100%, 50%);
}

/* Buttons and inputs */
.modal .lines-wrapper {
    position: relative;
}
.modal button.add-line,
.modal button.delete-line {
    min-width: 0;
    width: 1em;
    height: 1em;
    position: absolute;
    right: 0;
    bottom: 0.25em;
}
.modal button.add-line {
    z-index: 10;
}
.modal button.delete-line {
    background-color: transparent;
    color: hsl(0, 100%, 52%);
    right: 1em;
}
.modal button.delete-line:hover {
    color: hsl(0, 100%, 64%);
}
.modal .button-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.modal .button-wrapper button {
    width: 45%;
}
.modal input {
    width: calc(100% - 1em);
    margin-top: 0;
    border: 1px solid #666;
    padding-left: 2px;
}
.modal input.readonly {
    padding-left: 0;
    border: none;
}
</style>
