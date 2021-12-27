// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        edit_mode: false,
        add_mode: false,
        stats: []
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_edit_status = function (new_status){
        app.vue.edit_mode = new_status;
    }

    app.set_add_status = function (new_status){
        app.vue.add_mode = new_status;
    }

    app.stop_edit = function (){
        console.log(app.data.stats[0]['gpa'])
        axios.post(edit_stats_url,
            {
                id: app.data.stats[0]['id'],
                school: app.data.stats[0]['school'],
                grad_year: app.data.stats[0]['grad_year'],
                major: app.data.stats[0]['major'],
                sat_score: app.data.stats[0]['sat_score'],
                act_score: app.data.stats[0]['act_score'],
                gpa: app.data.stats[0]['gpa'],
            }).then(function (result) {
                app.vue.edit_mode = false
        });
    }

    // This contains all the methods.
    app.methods = {
        stop_edit: app.stop_edit,
        set_edit_status: app.set_edit_status,
        set_add_status: app.set_add_status,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // Call to the initializer.
    app.init = () => {
        // Get stats
        axios.get(load_stats_url)
        .then(function (response) {
            // app.vue.rows = app.enumerate(response.data.rows);
            let rows = response.data.stats;
            app.vue.stats = rows;
        })
    };

    app.init()
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
