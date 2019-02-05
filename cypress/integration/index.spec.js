describe('Index', () => {

  it('users should be able to view the "/" page', () => {
    cy
      .visit('/')
      .get('h2').contains('All Users');
  });

});