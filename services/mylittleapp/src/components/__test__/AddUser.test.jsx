import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import AddUser from '../AddUser';

test('AddUser renders a snapshot properly', () => {
    const tree = renderer.create(<AddUser/>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  
