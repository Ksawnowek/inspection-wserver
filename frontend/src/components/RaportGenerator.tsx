// components/RaportGenerator.tsx
import React, { useState } from 'react';
import { api } from '../api/client';
import { Button } from 'react-bootstrap';
import toast from 'react-hot-toast';

interface RaportGeneratorProps {
  zadanieId: number;
  kategoria: string;
  protokolId?: number;
}

export const RaportGenerator: React.FC<RaportGeneratorProps> = ({
  zadanieId,
  kategoria,
  protokolId
}) => {
  const [loading, setLoading] = useState(false);

  const generateReport = async (type: string) => {
    setLoading(true);
    try {
      const id = type === 'konserwacja' ? protokolId : zadanieId;

      const response = await api.post(
        `/raporty/generuj/${type}/${id}`,
        {},
        { responseType: 'blob' }
      );

      // Pobierz plik PDF
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${type}_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      toast.success('Raport wygenerowany pomyślnie!');
    } catch (error: any) {
      console.error('Błąd generowania raportu:', error);
      toast.error(`Błąd generowania raportu: ${error?.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const getAvailableReports = () => {
    const reports = [];
    
    if (kategoria === 'AWARIA') {
      reports.push({
        type: 'awaria',
        name: 'Raport Awarii',
        icon: '🔧'
      });
    }
    
    if (kategoria === 'PRACE_ROZNE') {
      reports.push({
        type: 'prace_rozne',
        name: 'Raport Prac Różnych',
        icon: '📝'
      });
    }
    
    if (kategoria === 'KONSERWACJA' && protokolId) {
      reports.push({
        type: 'konserwacja',
        name: 'Protokół Konserwacji',
        icon: '📋'
      });
    }
    
    if (kategoria === 'MONTAZ') {
      reports.push({
        type: 'montaz',
        name: 'Raport Montażu',
        icon: '🏗️'
      });
    }
    
    return reports;
  };

  const availableReports = getAvailableReports();

  return (
    <div className="raport-generator">
      {availableReports.length === 0 ? (
        <p>Brak dostępnych raportów dla tego zadania</p>
      ) : (
        <div className="d-flex gap-2 flex-wrap">
          {availableReports.map(report => (
            <Button
              key={report.type}
              variant="success"
              onClick={() => generateReport(report.type)}
              disabled={loading}
            >
              <span className="me-2">{report.icon}</span>
              {loading ? 'Generowanie...' : report.name}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
};