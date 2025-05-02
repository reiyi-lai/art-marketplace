$(document).ready(function() {
    $("#search-form").submit(function(event) {
        let searchInput = $("#search-input").val().trim();
        if (searchInput === "") {
            event.preventDefault();
            $("#search-input").val("").focus();
        }
    });
    
    let popularTitles = ["Starry Night", "The Scream", "Water Lilies"];
    let popularItems = [];

    allItems.forEach(item => {
        if (popularTitles.indexOf(item.title) !== -1) {
            popularItems.push(item);
        }
    });
    $('#add-form').submit(function(e){
        e.preventDefault(); // Prevent normal submission
        // console.log("Ajax handler loaded");
        // let valid = true;
        // $(this).find('input, textarea').each(function(){
        //     if ($(this).val().trim() === "") {
        //         e.preventDefault();
        //         $(this).focus();
        //         alert("Error: " + $(this).attr('name') + " is empty.");
        //         return false;
        //     }
        // });
        var formData = $(this).serialize();
        $.ajax({
            url: "/add",
            type: "POST",
            data: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response){
                if(response.success){
                    $('#success-message').show();
                    // $('#view-new').attr('href', "/view/" + response.new_item.id);
                    let newUrl = '/view/' + response.new_item_id;
                    $('#success-message .alert-link').attr('href', newUrl);
                    // Clear all fields and focus on the first field
                    $('#add-form')[0].reset();
                    $('#title').focus();
                } 
            }
        });
    });
    // Ensure script runs only on homepage
    $('#popular-items').empty();
    popularItems.forEach(item => {
        $("#popular-items").append(`
            <div class="col-md-4 mb-3">
                <div class="card">
                    <a href="/view/${item.id}">
                        <img src="${item.media_url}" class="card-img-top popular-image" alt="${item.title}">
                    </a>
                    <div class="card-body">
                    <h5 class="card-title">
                        <a href="/view/${item.id}">${item.title}</a>
                    </h5>
                    <p class="card-text">${item.description}</p>
                    </div>
                </div>
            </div>
        `);
    });
});