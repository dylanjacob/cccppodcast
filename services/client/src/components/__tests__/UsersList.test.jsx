import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
  {
    'active': true,
    'email': 'dylan.jacob@bubblecore.net',
    'id': 1,
    'username': 'djacob'
  },
  {
    'active': true,
    'email': 'kwrussel@gmail.com',
    'id': 2,
    'username': 'kevin'
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  expect(wrapper.find('#user').length).toBe(users.length);
  expect(wrapper.find('#user td').get(0).props.children).toBe('djacob');
  expect(wrapper.find('#user td').get(1).props.children).toBe('dylan.jacob@bubblecore.net');
  expect(wrapper.find('#user td').get(2).props.children).toBe('YES');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});