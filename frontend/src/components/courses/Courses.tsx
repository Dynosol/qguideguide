import React from 'react';
import CoursesTable from './CoursesTable'; // Adjust the path based on your file structure
import '/src/assets/css/Courses.css';
import { Link } from 'react-router-dom'; // Import Link
import { useThemeContext } from '../../utils/themeHelper';
import { colorPalettes } from '../../utils/colors';

import { useState } from "react"
import { ChevronDown } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const Courses: React.FC = () => {
  const { mode } = useThemeContext();
  const [position, setPosition] = React.useState("weighted")
  const [open, setOpen] = useState(false)

  const getSortingText = (value: string) => {
    switch (value) {
      case "weighted":
        return "Sorting via weighted scores...";
      case "weighted-department":
        return "Sorting via intradepartment...";
      case "naive":
        return "Sorting via naive averages...";
      default:
        return "Sorting...";
    }
  };


  return (
    <div className="non-navbar">
      <div className="guide">
        <i>
          <Link to="/about" className="guide-link">
            <strong>Bold</strong> is a weighted score across all courses, <span style={{ color: colorPalettes[mode].harvard}}><b>Red</b></span> is department-weighted, and italics are a naive average.
          </Link>
        </i>

        <DropdownMenu open={open} onOpenChange={setOpen}>
          <DropdownMenuTrigger asChild>
            <Button 
              variant="link"
              size="sm"
              className="text-sm flex items-center justify-between gap-1 h-8 px-3"
            >
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-700 to-red-400 animate-pulse">
                {getSortingText(position)}
              </span>
              <ChevronDown 
                className={`h-5 w-5 transition-transform duration-200 ${open ? 'rotate-180' : ''}`} 
              />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56 p-1">
            <DropdownMenuRadioGroup value={position} onValueChange={setPosition}>
              <DropdownMenuRadioItem value="weighted" className="text-s py-1.5">
                Sort via weighted scores
              </DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="weighted-department" className="text-s py-1.5">
                Sort via intradepartment
              </DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="naive" className="text-s py-1.5">
                Sort via naive averages
              </DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>

        <i>
          <Link to="/about" className="guide-link">
            <u>Learn about letter grade calculations and more here</u>
          </Link>
        </i>
      </div>

      <div className="main-table">
          <CoursesTable position={position}/>
      </div>
    </div>
  );
};

export default Courses;
