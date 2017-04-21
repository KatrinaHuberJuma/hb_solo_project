describe("Admin Add New Cohort Test Suite", function(){
    it("should add the new cohort link to the dom", function () {
        var results = {
            string: "Word",
            createdId: 5
        };
        showNewCohort(results);
        expect($('#new-cohort').html()).toBe('<a href="/cohort5">Word</a>');
    }
        );
});

// describe("Admin Async spec", function () {
//     it ("should post to the '/add-cohort' route", function () {
//         expect(true).toEqual(false)
//     })
// })