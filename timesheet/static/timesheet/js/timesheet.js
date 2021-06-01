$(document).ready(function () {

    // Denotes total number of rows
    let rowIdx = 0;

    // jQuery button click event to add a row
    $('#addBtn').on('click', function () {

        // Adding a row inside the tbody.
        // language=HTML format=false
        $('#addColumn').append(`<div id="R${++rowIdx}" >
    <div class="row">
                <div class="col-md-3 col-lg-3">
                    <button class="btn btn-lg btn-default dropdown-toggle form-dontrol"
                            type="button" data-toggle="dropdown" aria-expanded="false">
                        Select Project and Task <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" role="menu">
                    </ul>
                </div>


                <div class="col-md-1 col-lg-1 " >
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1 ">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="...">
                </div>
                <div class="col-md-1 col-lg-1">
                    <input type="text" class="form-control"  aria-label="..." readonly>
                </div>
                <div class="col-md-1 col-lg-1">
                    <button type="button" class="btn btn-default form-control"
                            aria-label="Left Align">
                        <span class="glyphicon glyphicon-trash" aria-hidden="true" ></span>
                    </button>
                </div>

            </div>
             </div> `);
    });

    // jQuery button click event to remove a row.
    $('#addColumn').on('click', '.remove', function () {

        // Getting all the rows next to the row
        // containing the clicked button
        const child = $(this).closest('div').nextAll();

        // Iterating across all the rows
        // obtained to change the index
        child.each(function () {

            // Getting <div> id.
            const id = $(this).attr('id');

            // Getting the <input> inside the .row-index class.
            let {html} = $(this).children('.row-index').children('input'); // Gets the row number from <div> id.
            const dig = parseInt(id.substring(1));

            // Modifying row index.
            html(`Row ${dig - 1}`);

            // Modifying row id.
            $(this).attr('id', `R${dig - 1}`);
        });

        // Removing the current row.
        $(this).closest('div').remove();

        // Decreasing total number of rows by 1.
        rowIdx--;
    });
});