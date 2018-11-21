const itemName = 'state';

export const loadState = () => {
  try {
    const serializedState = localStorage.getItem(itemName);
    if (serializedState == null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch (err) {
    console.log('Error: Could not load State from local storage');
    return undefined;
  }
};

export const saveState = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem(itemName, serializedState);
  } catch (err) {
    console.log('Error: Could not save state to local storage.');
  }
};

export const deleteState = () => {
  try {
    localStorage.removeItem(itemName);
  } catch (err) {
    // ignore
  }
};
