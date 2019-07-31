
let Address
let ICT
let Race 
let Gender

let get_input = function() {
    Address = $("input#Address").val()
    ICT = $("select#ICT").val()
    Race = $("select#Race").val()
    Gender = $("select#Gender").val()
    let d = new Date()
    let dayofweek = d.getDay()
    let month = d.getMonth()
    let hour = d.getHours()
    return {'Address': Address,
            'ICT': ICT,
            'Race': Race,
            'Gender': Gender,
            "dayofweek": dayofweek,
            "month": month,
            "hour": hour} 
};

let send_inputs_json = function(coefficients) {
    $.ajax({
    url: '/solve',
    contentType: "application/json; charset=utf-8",
    type: 'POST',
    success: function(data) {
        display_solutions(data);
    },
    data: JSON.stringify(coefficients)
});
};

let display_solutions = function(solutions){
  
    $("span#solution").html("<h4 >Predicted Probabilities:</h4><em>No Force: </em> " + solutions.p0.toFixed(4) + "<br> <em>Level 1: </em> " +  solutions.p1.toFixed(4) + " <br><em>Level 2:</em> " + solutions.p2.toFixed(4)  + " <br>" + "<em>Level 3:</em> " + solutions.p3.toFixed(4)  + " <br> " + "<em>Level 4: </em>" + solutions.p4.toFixed(4) )
};
console.log("hello")
        $(document).ready(function() {


            $("#button2").click(function() {
                send_thank_you()
            })

            $("button#solve").click(function() {
                
                let coefficients = get_input();
                
                send_inputs_json(coefficients);
            })
})

        $(document).ready(function() {
          
       
       
        } )
let send_thank_you = function() {
    email = $("#email").val()
    console.log(email) 

    $("#email").val("Thank you!");

    window.localStorage.setItem(email, email)
    // $.ajax({
    //     url: '/button-addon2',
    //     contentType: "application/json; charset=utf-8",
    //     type: 'POST',
    //     success: function(data) {
            
    //     },
    // }) 
};

