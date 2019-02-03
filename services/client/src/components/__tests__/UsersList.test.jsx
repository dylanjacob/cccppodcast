import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
  {
    'admin': true,
    'active': true,
    'email': 'dylan.jacob@bubblecore.net',
    'id': 1,
    'username': 'djacob'
  },
  {
    'admin': false,
    'active': true,
    'email': 'kwrussel@gmail.com',
    'id': 2,
    'username': 'kevin'
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  expect(wrapper.find('h2').get(0).props.children).toBe('All Users');
  
  const table = wrapper.find('table');
  expect(table.length).toBe(1);

  expect(wrapper.find('thead').length).toBe(1);
  const th = wrapper.find('th[scope="col"]');
  expect(th.length).toBe(6);
  expect(th.get(0).props.children).toBe('#');
  expect(th.get(1).props.children).toBe('ID');
  expect(th.get(2).props.children).toBe('Username');
  expect(th.get(3).props.children).toBe('Email');
  expect(th.get(4).props.children).toBe('Active');
  expect(th.get(5).props.children).toBe('Admin');

  expect(wrapper.find('tbody').length).toBe(1);
  expect(wrapper.find('tbody > tr').length).toBe(2);
  const td = wrapper.find('tbody > tr > td');
  expect(td.length).toBe(10);
 
  expect(td.get(0).props.children).toBe(1);
  expect(td.get(1).props.children).toBe('djacob');
  expect(td.get(2).props.children).toBe('dylan.jacob@bubblecore.net');
  expect(td.get(3).props.children).toBe('YES');
  expect(td.get(4).props.children).toBe('YES');
  expect(td.get(5).props.children).toBe(2);
  expect(td.get(6).props.children).toBe('kevin');
  expect(td.get(7).props.children).toBe('kwrussel@gmail.com');
  expect(td.get(8).props.children).toBe('YES');
  expect(td.get(9).props.children).toBe('NO');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});