import React, { useCallback, useRef, useState } from 'react';
import Shell from './Shell.jsx';
import SourceSheet from './SourceSheet.jsx';

export default function App() {
  const [sourceId, setSourceId] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);
  const draftsRef = useRef({});

  const openSource = useCallback((id, trigger) => {
    if (trigger) triggerRef.current = trigger;
    setSourceId(id);
    setIsOpen(true);
  }, []);

  const closeSource = useCallback(() => {
    setIsOpen(false);
    window.requestAnimationFrame(() => triggerRef.current?.focus({ preventScroll: true }));
  }, []);

  return (
    <>
      <Shell onOpenSource={openSource} />
      {isOpen && <SourceSheet sourceId={sourceId} onSelectSource={(id) => openSource(id)} onClose={closeSource} draftsRef={draftsRef} />}
    </>
  );
}
