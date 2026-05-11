import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock('react-markdown', () => {
  // CRA/Jest can choke on ESM builds of react-markdown.
  // For this app smoke test, a simple passthrough is enough.
  // eslint-disable-next-line react/display-name
  return function MockMarkdown({ children }) {
    return children ?? null;
  };
});

jest.mock('lucide-react', () => ({
  MessageCircle: () => null,
  Send: () => null,
}));

test('renders inventory section', () => {
  render(<App />);
  expect(screen.getByText(/featured inventory/i)).toBeInTheDocument();
});
